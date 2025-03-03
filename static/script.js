let currentDepartment = null;

function commentDepartment(departmentId) {
    currentDepartment = departmentId;
    document.getElementById("commentModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("commentModal").style.display = "none";
}

async function submitComment() {
    const comment = document.getElementById("commentText").value;
    if (!comment.trim()) {
        alert("El comentario no puede estar vacío.");
        return;
    }

    const response = await fetch(`/comment/${currentDepartment}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comentario: comment })
    });

    if (response.ok) {
        closeModal();
        location.reload();
    } else {
        alert("Error al enviar el comentario.");
    }
}

let removeTimeout; // Variable para almacenar el temporizador

async function rejectDepartment(departmentId) {
    const response = await fetch(`/reject/${departmentId}`, {
        method: 'POST'
    });
    if (response.ok) {
        alert(`Departamento ${departmentId} rechazado`);
        location.reload();  // Recargar la página para reflejar los cambios
    } else {
        alert('Error al rechazar el departamento');
    }
}

async function favoriteDepartment(departmentId) {
    const response = await fetch(`/favorite/${departmentId}`, {
        method: 'POST'
    });
    if (response.ok) {
        alert(`Departamento ${departmentId} marcado como favorito`);
        location.reload();  // Recargar la página para reflejar los cambios
    } else {
        alert('Error al marcar el departamento como favorito');
    }
}

async function shareDepartment(departmentId) {
    const url = `https://scarpdepto.vercel.app/departments/${departmentId}`;
    
    if (navigator.share) {
        try {
            await navigator.share({
                title: "Departamento en alquiler",
                text: "Mira este departamento que encontré:",
                url: url
            });
            console.log("Compartido exitosamente");
        } catch (error) {
            console.error("Error al compartir:", error);
        }
    } else {
        // Si no es compatible, copiar al portapapeles
        try {
            await navigator.clipboard.writeText(url);
            alert("Enlace copiado al portapapeles");
        } catch (error) {
            console.error("Error al copiar el enlace:", error);
            alert("No se pudo copiar el enlace");
        }
    }
}

async function removeDepartment(departmentId) {
    const response = await fetch(`/remove/${departmentId}`, {
        method: 'POST'
    });
    if (response.ok) {
        alert(`Departamento ${departmentId} removido correctamente`);
        location.reload();  // Recargar la página para reflejar los cambios
    } else {
        alert('Error al remover el departamento como favorito');
    }
    window.location.href = "https://scarpdepto.vercel.app/departments";
}

async function backToDepartments(person) {
    window.location.href = "https://scarpdepto.vercel.app/departments";
}

async function goToSeleccionarPersona() {
    window.location.href = "https://scarpdepto.vercel.app/seleccionar-persona";
}

function startRemoveTimer(departmentId) {
    rejectTimeout = setTimeout(() => {
        removeDepartment(departmentId);
    }, 3000); // Espera 2 segundos antes de ejecutar la acción
}

function clearRemoveTimer() {
    clearTimeout(removeTimeout); // Cancela la acción si se suelta antes
}

async function removeDepartment(departmentId) {
    const response = await fetch(`/remove/${departmentId}`, {
         method: 'POST'
    });

    if (response.ok) {
        alert(`Departamento ${departmentId} removido`);
        location.reload();
    } else {
        alert('Error al remover el departamento');
    }
}

async function setPersonCookie() {
    const person = document.getElementById("personSelector").value;
    document.cookie = `person=${encodeURIComponent(person)}; path=/; max-age=31536000`; // Expira en 1 año

    window.location.href = "https://scarpdepto.vercel.app/departments";
}

function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        const [key, value] = cookie.split("=");
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null; // Retorna null si la cookie no existe
}