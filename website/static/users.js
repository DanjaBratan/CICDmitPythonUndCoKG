// JavaScript-Funktion zum Löschen eines Users
function deleteUser(userId) {
    // Eine Anfrage an den Server senden, um den User zu löschen
    fetch('/delete-user/' + userId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((_res) => {
      window.location.href = "/"; // Die Seite neu laden, um die aktualisierte Liste der Notizen anzuzeigen
    });
}

// JavaScript-Funktion zum Aktualisieren der Mail eines Users
function updateUserEmail(userId) {
  var newMail = prompt("Schreibe die neue Mail:");
  if (newMail != null) {
      fetch('/update-user-email/'+ userId, {
          method: 'POST',
          body: JSON.stringify({userId: userId, newMail: newMail}),
          headers: {
            'Content-Type': 'application/json'
          }
      })
      .then((_res) => {
        window.location.href = "/"; // Die Seite neu laden, um die aktualisierte Liste der Notizen anzuzeigen
      });
  }
}