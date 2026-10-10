/**
 * drag_drop.js
 * -------------
 * Owner: Person 4
 *
 * Drag-and-drop for cards between lists, using the SortableJS library,
 * connected to Person 2's /card/<card_id>/move endpoint.
 *
 * WHAT THE HTML NEEDS (board.html, Person 3):
 *   - SortableJS loaded BEFORE this file (in base.html):
 *       <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
 *   - One element per list with class "list-column" and the list's id:
 *       <div class="list-column" data-list-id="{{ list._id }}"> ... </div>
 *   - Every card inside it with the card's id:
 *       <div class="card" data-card-id="{{ card._id }}"> ... </div>
 *
 * HOW IT WORKS:
 *   1. Every .list-column becomes a Sortable drop zone. They all share the
 *      group name "cards", so a card can move from one list to another.
 *   2. Only elements with data-card-id can be dragged, so headers or
 *      "add card" forms inside a column stay where they are.
 *   3. When a card is dropped in a DIFFERENT list, we POST the new list id
 *      to /card/<card_id>/move.
 *   4. If the server says no (or the request fails), the card is put back
 *      where it was, so the page never shows something the database doesn't have.
 */

document.addEventListener("DOMContentLoaded", function () {
    if (typeof Sortable === "undefined") {
        console.error("drag_drop.js: SortableJS is not loaded. Add its <script> tag before this file.");
        return;
    }

    const listColumns = document.querySelectorAll(".list-column");

    listColumns.forEach(function (column) {
        new Sortable(column, {
            group: "cards",
            animation: 150,
            draggable: "[data-card-id]",
            onEnd: handleCardDrop,
        });
    });
});


function handleCardDrop(evt) {
    // Dropped back into the same list: nothing changes in the database.
    if (evt.from === evt.to) {
        return;
    }

    const cardId = evt.item.dataset.cardId;
    const newListId = evt.to.dataset.listId;

    if (!cardId || !newListId) {
        console.error("drag_drop.js: missing data-card-id or data-list-id in the HTML.");
        revertMove(evt);
        return;
    }

    fetch(`/card/${cardId}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_list_id: newListId }),
    })
        .then(function (res) {
            if (!res.ok) {
                throw new Error(`Server responded with status ${res.status}`);
            }
            return res.json();
        })
        .then(function (data) {
            if (!data.success) {
                throw new Error("Server did not confirm the move");
            }
            console.log("Card moved:", cardId, "->", newListId);
        })
        .catch(function (err) {
            console.error("Move failed, putting the card back:", err);
            revertMove(evt);
        });
}


// Put the card back in its original list, at its original position.
function revertMove(evt) {
    const originalList = evt.from;
    const elementAtOldPosition = originalList.children[evt.oldIndex] || null;
    originalList.insertBefore(evt.item, elementAtOldPosition);
}
