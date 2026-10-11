/**
 * card_dialog.js
 * ---------------
 * Owner: Person 4 (task A3)       Practice first: Tarmo_V2_Warmup.ipynb, 4C
 *
 * The card dialog: open it, fill it from the server, tick checklist items,
 * and send comments, all without reloading the page.
 *
 * Needs from the other people:
 *   - Person 2's routes (see the API table in docs/v2/TASKS.md)
 *   - Person 3's element ids: #card-dialog, #dialog-title, #dialog-description,
 *     #checklist, #bar, #badge, #checklist-form, #comment-form, #timeline
 *
 * TODO (Person 4):
 *   1. openCard(cardId)
 *        fetch(`/card/${cardId}/json`) -> fill the title, description,
 *        checklist items, progress bar and timeline; then show the dialog
 *        (remove Tailwind class "hidden").
 *   2. toggleItem(cardId, itemId)
 *        POST /card/<id>/checklist/<item>/toggle -> returns {done,total,percent}
 *        -> set #bar width and #badge text ("2/5").
 *   3. addItem(cardId, text)  and  deleteItem(cardId, itemId)  (same idea)
 *   4. sendComment(cardId, text)
 *        POST JSON {text} to /card/<id>/comment -> add the new bubble on top.
 *   5. closeDialog()  (close button and the Escape key)
 *
 * Always check `res.ok` and show a short message if a request failed.
 */

// async function openCard(cardId) { ... }
