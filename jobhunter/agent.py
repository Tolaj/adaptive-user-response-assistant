# jobhunter/agent.py
# ─────────────────────────────────────────────────────────────────────────────
# The core VLM agent loop.
# Takes ONE screenshot → asks VLM what to do → executes → repeats.
# This is the "eyes + brain" of the job hunter.
#
# Flow per site per query:
#   1. Navigate to site
#   2. VLM sees page → decides: type search / click / scroll / extract / done
#   3. Execute action
#   4. Repeat until VLM says "extract" or "done" or max actions reached
#   5. Extract job listings from page
#   6. Score each job against profile
#   7. Save high-scoring jobs to CSV
# ─────────────────────────────────────────────────────────────────────────────

import time
from jobhunter.config import MAX_ACTIONS_PER_PAGE, MAX_JOBS_PER_SITE, MIN_SCORE_TO_SAVE
from jobhunter.vlm_query import decide_action, extract_jobs_from_page, score_job
from jobhunter.actions import execute_action
from jobhunter.storage import save_job, is_seen
from jobhunter.logger import log


# ── Entry URLs per site ────────────────────────────────────────────────────
SITE_URLS = {
    "linkedin":  "https://www.linkedin.com/jobs",
    "indeed":    "https://www.indeed.com",
    "naukri":    "https://www.naukri.com",
    "wellfound": "https://wellfound.com/jobs",
}


def hunt_site(site: str, query: str, profile: dict) -> int:
    """
    Run the VLM agent on one site with one search query.
    Returns the number of NEW jobs saved.
    """
    from jobhunter.browser import navigate

    log(f"[{site.upper()}] Starting hunt for: '{query}'")

    # ── Step 1: Navigate to site ──────────────────────────────────────────
    url = SITE_URLS.get(site, "https://www.google.com")
    navigate(url)

    # ── Step 2: VLM action loop ───────────────────────────────────────────
    goal = (
        f"Search for '{query}' jobs on this site. "
        f"Type the query in the search box, press enter, "
        f"then scroll through results. "
        f"When you can see job listings, say action=extract."
    )

    jobs_saved = 0
    total_extracted = 0

    for step in range(MAX_ACTIONS_PER_PAGE):
        log(f"[{site.upper()}] Step {step+1}/{MAX_ACTIONS_PER_PAGE}")

        action = decide_action(goal)
        action_type = action.get("action", "unknown")

        if action_type == "done":
            log(f"[{site.upper()}] VLM says done.")
            break

        if action_type == "extract":
            # ── Step 3: Extract jobs from current page view ───────────────
            log(f"[{site.upper()}] Extracting jobs from page...")
            jobs = extract_jobs_from_page()
            total_extracted += len(jobs)

            # ── Step 4: Score and save each job ───────────────────────────
            for job in jobs:
                title   = job.get("title", "")
                company = job.get("company", "")

                if not title or not company:
                    continue

                # Skip if already seen
                if is_seen(title, company, site):
                    log(f"  [SKIP] Already seen: {title} @ {company}")
                    continue

                # Quick keyword filter before spending VLM tokens on scoring
                avoid = profile.get("avoid_keywords", [])
                combined_text = f"{title} {job.get('snippet', '')}".lower()
                if any(kw.lower() in combined_text for kw in avoid):
                    log(f"  [SKIP] Avoided keyword in: {title}")
                    continue

                # Score the job
                score_result = score_job(job, profile)
                score        = int(score_result.get("score", 5))
                reason       = score_result.get("reason", "")

                if score >= MIN_SCORE_TO_SAVE:
                    saved = save_job(job, site, score, reason)
                    if saved:
                        jobs_saved += 1
                        log(f"  [SAVED ★{score}] {title} @ {company} — {reason}")
                    else:
                        log(f"  [DUP] {title} @ {company}")
                else:
                    log(f"  [LOW ★{score}] {title} @ {company} — {reason}")

                if total_extracted >= MAX_JOBS_PER_SITE:
                    log(f"[{site.upper()}] Reached max jobs limit ({MAX_JOBS_PER_SITE})")
                    return jobs_saved

            # After extraction, scroll to see more jobs
            goal = (
                "Scroll down to see more job listings. "
                "If more listings are visible, say action=extract again. "
                "If no more listings, say action=done."
            )

        else:
            # Execute navigation action (click, type, scroll, wait, navigate)
            execute_action(action)

    log(f"[{site.upper()}] Done. Saved {jobs_saved} new jobs from '{query}'.")
    return jobs_saved


def run_full_hunt(profile: dict, search_queries: dict) -> dict:
    """
    Run the full job hunt across all sites and all queries.
    Returns a summary dict.
    """
    from jobhunter.storage import get_stats

    summary = {}
    total_new = 0

    for site, queries in search_queries.items():
        site_new = 0
        for query in queries:
            try:
                new = hunt_site(site, query, profile)
                site_new += new
                total_new += new
                # Small pause between queries — be polite to the server
                time.sleep(3)
            except Exception as e:
                log(f"[ERROR] {site} / '{query}': {e}")
        summary[site] = site_new
        log(f"[SUMMARY] {site}: {site_new} new jobs")

    stats = get_stats()
    log(
        f"\n{'='*50}\n"
        f"HUNT COMPLETE\n"
        f"  New this run:  {total_new}\n"
        f"  Found today:   {stats['today']}\n"
        f"  Total in DB:   {stats['total']}\n"
        f"{'='*50}\n"
    )

    return {"new_this_run": total_new, "stats": stats, "by_site": summary}