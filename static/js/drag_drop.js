/**
 * drag_drop.js
 * -------------
 * Owner: Person 4
 *
 * Drag-and-drop for cards between lists, using the SortableJS library,
 * connected to Person 2's /card/<card_id>/move endpoint.
 *
 * SETUP:
 *   1. Add SortableJS via CDN in base.html (Person 3 coordinates this):
 *      <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
 *   2. This file runs after the page loads and turns every `.list-column`
 *      into a drop zone that cards can move between.
 *
 * TASK FOR PERSON 4:
 *   1. Select all elements with class "list-column" (one per Mongo list)
 *   2. For each one, create a `new Sortable(element, {...})` that:
 *        - shares a "group" name across all lists (so cards can move
 *          between them, not just reorder within one)
 *        - has an `onEnd` callback that fires when a card is dropped
 *   3. In onEnd, read:
 *        - evt.item.dataset.cardId       (which card moved)
 *        - evt.to.dataset.listId           (which list it was dropped into)
 *   4. Send that to the backend with fetch():
 *        fetch(`/card/${cardId}/move`, {
 *          method: "POST",
 *          headers: { "Content-Type": "application/json" },
 *          body: JSON.stringify({ new_list_id: newListId })
 *        })
 *   5. Handle the response (e.g. log an error and revert the UI if it fails)
 */

document.addEventListener("DOMContentLoaded", function () {
    const listColumns = document.querySelectorAll(".list-column");

    listColumns.forEach(function (column) {
        // TODO (Person 4): initialize Sortable on `column` here
        // new Sortable(column, {
        //     group: "cards",
        //     animation: 150,
        //     onEnd: function (evt) {
        //         const cardId = evt.item.dataset.cardId;
        //         const newListId = evt.to.dataset.listId;
        //
        //         fetch(`/card/${cardId}/move`, {
        //             method: "POST",
        //             headers: { "Content-Type": "application/json" },
        //             body: JSON.stringify({ new_list_id: newListId }),
        //         })
        //             .then((res) => res.json())
        //             .then((data) => console.log("Card moved:", data))
        //             .catch((err) => console.error("Move failed:", err));
        //     },
        // });
    });
});
