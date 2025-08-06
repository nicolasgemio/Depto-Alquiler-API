let currentSearchDepartmentId = null;

function commentDepartment(departmentId) {
    currentSearchDepartmentId = departmentId;
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

    const response = await fetch(`/comment/${currentSearchDepartmentId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ commentary: comment })
    });

    if (response.ok) {
        closeModal();
        location.reload();
    } else {
        alert("Error al enviar el comentario.");
    }
}

let removeTimeout; // Variable para almacenar el temporizador

async function rejectDepartment(search_department_id) {
    const response = await fetch(`/reject/${search_department_id}`, {
        method: 'POST'
    });

    const data = await response.json();

    if (response.ok) {
        alert(`✅ ${data.mensaje}`);
        location.reload();
    } else {
        alert(`❌ ${data.mensaje}`);
    }
}

async function favoriteDepartment(search_department_id) {
    const response = await fetch(`/favorite/${search_department_id}`, {
        method: 'POST'
    });

    const data = await response.json();

    if (response.ok) {
        alert(`✅ ${data.mensaje}`);
        location.reload();
    } else {
        alert(`❌ ${data.mensaje}`);
    }
}

async function shareDepartment(departmentId) {
    const url = `$/departments/${departmentId}`;
    
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

async function goToDepartments(seach_id) {
    window.location.href = `/departments?search_id=${seach_id}`;
}

async function goToSeleccionarPersona() {
    window.location.href = `/seleccionar-persona/`;
}

async function removeDepartment(searchDepartmentId, search_id) {
    const response = await fetch(`/remove/${searchDepartmentId}`, {
         method: 'POST'
    });
    
    const data = await response.json();

    if (response.ok) {
        alert(`✅ ${data.mensaje}`);
        location.reload()
        window.location.href =  `/departments?search_id=${search_id}`;
        
    } else {
        alert('Error al remover el departamento');
    }
}

async function setPersonCookie() {
    const person = document.getElementById("personSelector").value;
    document.cookie = `person=${encodeURIComponent(person)}; path=/; max-age=31536000`; // Expira en 1 año

    window.location.href = `/departments/`;}

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

function logut() {
    window.location.href = '/auth/logout';
}