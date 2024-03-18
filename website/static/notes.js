// JavaScript-Funktion zum Löschen einer Notiz
function deleteNote(noteId) {
    // Eine Anfrage an den Server senden, um die Notiz zu löschen
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }), // Die zu sendenden Daten in JSON-Format umwandeln und als Body der Anfrage setzen
    }).then((_res) => {
      window.location.href = "/"; // Die Seite neu laden, um die aktualisierte Liste der Notizen anzuzeigen
    });
}

function updateNote(noteId) {
  var newNote = prompt("Schreibe die aktualisierte Notiz:");
  if (newNote != null) {
      fetch('/update-note/'+ noteId, {
          method: 'POST',
          body: JSON.stringify({noteId: noteId, newNote: newNote}),
          headers: {
            'Content-Type': 'application/json'
          }
      })
      .then((_res) => {
        window.location.href = "/"; // Die Seite neu laden, um die aktualisierte Liste der Notizen anzuzeigen
      });
  }
}