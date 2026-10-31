/**
 * filter.js
 * ----------
 * Owner: Person 4 (task A4)       Practice first: Tarmo_V2_Warmup.ipynb, 4C
 *
 * The filter bar under the navbar.
 * Needs Person 3's ids: #search, #filter-member, #filter-label, #filter-due,
 * #clear-filters. Cards have the class ".card".
 *
 * TODO (Person 4):
 *   1. Live text filter (no server call): on every "input" event of #search,
 *      hide each ".card" whose text does not include the search text.
 *   2. Member / label / due-date filters: fetch
 *        `/board/${boardId}/cards?text=&member=&label=&due_before=`
 *      (Person 2's filter_cards route) and show only the returned card ids.
 *   3. "Clear filters" resets every input and shows all cards again.
 */
