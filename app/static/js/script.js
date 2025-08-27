const API_BASE = '/api/v1/events';

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadEvents();
    setupEventListeners();
    setupCharacterCounters();
});

// Настройка счетчиков символов
function setupCharacterCounters() {
    const titleInput = document.getElementById('title');
    const textInput = document.getElementById('text');
    const editTitleInput = document.getElementById('editTitle');
    const editTextInput = document.getElementById('editText');

    titleInput.addEventListener('input', updateCharCounter.bind(null, 'titleCounter', 30));
    textInput.addEventListener('input', updateCharCounter.bind(null, 'textCounter', 200));
    editTitleInput.addEventListener('input', updateCharCounter.bind(null, 'editTitleCounter', 30));
    editTextInput.addEventListener('input', updateCharCounter.bind(null, 'editTextCounter', 200));
}

function updateCharCounter(counterId, maxLength, event) {
    const counter = document.getElementById(counterId);
    const length = event.target.value.length;
    counter.textContent = `${length}/${maxLength}`;
    
    if (length > maxLength * 0.8) {
        counter.style.color = '#dc3545';
    } else {
        counter.style.color = '#6c757d';
    }
}

// Настройка обработчиков событий
function setupEventListeners() {
    // Форма добавления события
    document.getElementById('eventForm').addEventListener('submit', handleAddEvent);
    
    // Форма редактирования события
    document.getElementById('editForm').addEventListener('submit', handleEditEvent);
    
    // Закрытие модального окна
    document.querySelector('.close').addEventListener('click', closeModal);
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('editModal')) {
            closeModal();
        }
    });
}

// Загрузка всех событий
async function loadEvents() {
    try {
        const response = await fetch(API_BASE + '/');
        if (!response.ok) throw new Error('Ошибка загрузки событий');
        
        const data = await response.text();
        const events = parseEventsData(data);
        displayEvents(events);
    } catch (error) {
        showError('Ошибка при загрузке событий: ' + error.message);
    }
}

// Парсинг данных событий
function parseEventsData(rawData) {
    if (!rawData.trim()) return [];
    
    return rawData.trim().split('\n').map(line => {
        const parts = line.split('|');
        if (parts.length === 4) {
            return { id: parts[0], date: parts[1], title: parts[2], text: parts[3] };
        } else if (parts.length === 3) {
            return { id: null, date: parts[0], title: parts[1], text: parts[2] };
        }
        return null;
    }).filter(event => event !== null);
}

// Отображение событий
function displayEvents(events) {
    const eventsList = document.getElementById('eventsList');
    const monthFilter = document.getElementById('monthFilter').value;
    
    if (events.length === 0) {
        eventsList.innerHTML = '<p class="loading">Событий пока нет</p>';
        return;
    }

    // Фильтрация по месяцу
    let filteredEvents = events;
    if (monthFilter) {
        filteredEvents = events.filter(event => event.date.startsWith(monthFilter));
    }

    eventsList.innerHTML = filteredEvents.map(event => `
        <div class="event-card">
            <div class="event-date">📅 ${formatDate(event.date)}</div>
            <h3 class="event-title">${escapeHtml(event.title)}</h3>
            <p class="event-text">${escapeHtml(event.text)}</p>
            <div class="event-actions">
                <button class="btn-edit" onclick="openEditModal('${event.id}', '${event.date}', '${escapeHtml(event.title)}', '${escapeHtml(event.text)}')">
                    ✏️ Редактировать
                </button>
                <button class="btn-delete" onclick="deleteEvent('${event.id}')">
                    🗑️ Удалить
                </button>
            </div>
        </div>
    `).join('');
}

// Фильтрация событий по месяцу
function filterEvents() {
    loadEvents();
}

// Добавление нового события
async function handleAddEvent(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const date = formData.get('date');
    const title = formData.get('title');
    const text = formData.get('text');
    
    // Валидация
    if (!validateEvent(date, title, text)) return;
    
    try {
        const rawData = `${date}|${title}|${text}`;
        const response = await fetch(API_BASE + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: rawData
        });
        
        if (response.ok) {
            showSuccess('Событие успешно добавлено!');
            event.target.reset();
            updateCharCounter('titleCounter', 30, { target: { value: '' } });
            updateCharCounter('textCounter', 200, { target: { value: '' } });
            loadEvents();
        } else {
            const errorText = await response.text();
            throw new Error(errorText);
        }
    } catch (error) {
        showError('Ошибка при добавлении события: ' + error.message);
    }
}

// Открытие модального окна для редактирования
function openEditModal(id, date, title, text) {
    document.getElementById('editId').value = id;
    document.getElementById('editDate').value = date;
    document.getElementById('editTitle').value = title;
    document.getElementById('editText').value = text;
    
    // Обновляем счетчики символов
    updateCharCounter('editTitleCounter', 30, { target: { value: title } });
    updateCharCounter('editTextCounter', 200, { target: { value: text } });
    
    document.getElementById('editModal').style.display = 'block';
}

// Закрытие модального окна
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Редактирование события
async function handleEditEvent(event) {
    event.preventDefault();
    
    const id = document.getElementById('editId').value;
    const formData = new FormData(event.target);
    const date = formData.get('date');
    const title = formData.get('title');
    const text = formData.get('text');
    
    if (!validateEvent(date, title, text)) return;
    
    try {
        const rawData = `${date}|${title}|${text}`;
        const response = await fetch(API_BASE + '/' + id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'text/plain'
            },
            body: rawData
        });
        
        if (response.ok) {
            showSuccess('Событие успешно обновлено!');
            closeModal();
            loadEvents();
        } else {
            const errorText = await response.text();
            throw new Error(errorText);
        }
    } catch (error) {
        showError('Ошибка при обновлении события: ' + error.message);
    }
}

// Удаление события
async function deleteEvent(id) {
    if (!confirm('Вы уверены, что хотите удалить это событие?')) return;
    
    try {
        const response = await fetch(API_BASE + '/' + id + '/', {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showSuccess('Событие успешно удалено!');
            loadEvents();
        } else {
            const errorText = await response.text();
            throw new Error(errorText);
        }
    } catch (error) {
        showError('Ошибка при удалении события: ' + error.message);
    }
}

// Валидация данных события
function validateEvent(date, title, text) {
    if (!date) {
        showError('Пожалуйста, выберите дату');
        return false;
    }
    
    if (!title.trim()) {
        showError('Заголовок не может быть пустым');
        return false;
    }
    
    if (title.length > 30) {
        showError('Заголовок не может превышать 30 символов');
        return false;
    }
    
    if (!text.trim()) {
        showError('Описание не может быть пустым');
        return false;
    }
    
    if (text.length > 200) {
        showError('Описание не может превышать 200 символов');
        return false;
    }
    
    return true;
}

// Форматирование даты
function formatDate(dateString) {
    const date = new Date(dateString + 'T00:00:00');
    return date.toLocaleDateString('ru-RU', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Экранирование HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Показать сообщение об ошибке
function showError(message) {
    showMessage(message, 'error');
}

// Показать сообщение об успехе
function showSuccess(message) {
    showMessage(message, 'success');
}

// Показать сообщение
function showMessage(message, type) {
    // Удаляем предыдущие сообщения
    const existingMessages = document.querySelectorAll('.error, .success');
    existingMessages.forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    
    // Вставляем сообщение после заголовка соответствующей секции
    const targetSection = type === 'error' ? '.form-section' : '.events-section';
    const section = document.querySelector(targetSection);
    const heading = section.querySelector('h2');
    heading.parentNode.insertBefore(messageDiv, heading.nextSibling);
    
    // Автоматически скрываем через 5 секунд
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}