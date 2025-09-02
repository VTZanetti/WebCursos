/**
 * WebCursos JavaScript Interactivity
 * Handles real-time lesson progress updates and notes functionality
 */

class WebCursosApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFlashMessages();
    }

    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        // Lesson checkbox event listeners
        this.setupLessonCheckboxes();
        
        // Notes functionality
        this.setupNotesHandlers();
        
        // Form enhancements
        this.setupFormEnhancements();
    }

    /**
     * Setup lesson checkbox click handlers for real-time updates
     */
    setupLessonCheckboxes() {
        const checkboxes = document.querySelectorAll('.lesson-checkbox');
        
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', async (e) => {
                e.preventDefault(); // Prevent form submission
                
                const isChecked = checkbox.checked;
                const lessonItem = checkbox.closest('.lesson-item');
                const form = checkbox.closest('form');
                
                // Extract course ID and lesson number from the form action
                const actionUrl = form.action;
                const urlParts = actionUrl.split('/');
                const cursoId = urlParts[urlParts.length - 2];
                const numeroAula = urlParts[urlParts.length - 1];
                
                // Show loading state
                this.setLessonLoadingState(lessonItem, true);
                
                try {
                    // Send AJAX request to update lesson status
                    const response = await this.updateLessonStatus(cursoId, numeroAula, isChecked);
                    
                    if (response.success) {
                        // Update UI without page reload
                        this.updateLessonUI(lessonItem, isChecked);
                        this.updateProgressBar(response.progress);
                        this.updateProgressStats(response.completed_count, response.total_aulas, response.progress);
                        
                        // Show success message
                        this.showNotification(response.message, 'success');
                    } else {
                        // Revert checkbox state on error
                        checkbox.checked = !isChecked;
                        this.showNotification(response.message || 'Erro ao atualizar aula', 'error');
                    }
                } catch (error) {
                    console.error('Error updating lesson:', error);
                    checkbox.checked = !isChecked; // Revert checkbox state
                    this.showNotification('Erro de conexão. Tente novamente.', 'error');
                } finally {
                    this.setLessonLoadingState(lessonItem, false);
                }
            });
        });
    }

    /**
     * Send AJAX request to update lesson status
     */
    async updateLessonStatus(cursoId, numeroAula, isCompleted) {
        const response = await fetch('/atualizar_aula', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                curso_id: parseInt(cursoId),
                numero_aula: parseInt(numeroAula),
                completed: isCompleted
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Update lesson item UI based on completion status
     */
    updateLessonUI(lessonItem, isCompleted) {
        const statusElement = lessonItem.querySelector('.lesson-status');
        
        if (isCompleted) {
            lessonItem.classList.add('completed');
            statusElement.textContent = '✓ Concluída';
            statusElement.className = 'lesson-status status-completed';
        } else {
            lessonItem.classList.remove('completed');
            statusElement.textContent = '⏳ Pendente';
            statusElement.className = 'lesson-status status-pending';
        }
    }

    /**
     * Update progress bar with new percentage
     */
    updateProgressBar(progressPercentage) {
        const progressFills = document.querySelectorAll('.progress-fill');
        progressFills.forEach(fill => {
            fill.style.width = `${progressPercentage}%`;
        });
    }

    /**
     * Update progress statistics in the UI
     */
    updateProgressStats(completedCount, totalAulas, progressPercentage) {
        // Update summary cards
        const completedCard = document.querySelector('.summary-card.completed .summary-number');
        const pendingCard = document.querySelector('.summary-card.pending .summary-number');
        const progressCard = document.querySelector('.summary-card.progress .summary-number');
        
        if (completedCard) completedCard.textContent = completedCount;
        if (pendingCard) pendingCard.textContent = totalAulas - completedCount;
        if (progressCard) progressCard.textContent = `${progressPercentage}%`;
        
        // Update progress text
        const progressTexts = document.querySelectorAll('.progress-text');
        progressTexts.forEach(text => {
            text.textContent = `${completedCount} de ${totalAulas} aulas concluídas (${progressPercentage}%)`;
        });
        
        // Update lessons stats
        const lessonsStats = document.querySelector('.lessons-stats');
        if (lessonsStats) {
            lessonsStats.textContent = `${completedCount}/${totalAulas} concluídas`;
        }
    }

    /**
     * Set loading state for lesson item
     */
    setLessonLoadingState(lessonItem, isLoading) {
        if (isLoading) {
            lessonItem.style.opacity = '0.6';
            lessonItem.style.pointerEvents = 'none';
        } else {
            lessonItem.style.opacity = '1';
            lessonItem.style.pointerEvents = 'auto';
        }
    }

    /**
     * Setup notes functionality
     */
    setupNotesHandlers() {
        const notesTextarea = document.getElementById('course-notes');
        const saveNotesBtn = document.getElementById('save-notes-btn');
        
        if (notesTextarea && saveNotesBtn) {
            // Auto-save notes on typing (debounced)
            let saveTimeout;
            notesTextarea.addEventListener('input', () => {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    this.autoSaveNotes();
                }, 2000); // Auto-save after 2 seconds of inactivity
            });
            
            // Manual save button
            saveNotesBtn.addEventListener('click', () => {
                this.saveNotes();
            });
        }
    }

    /**
     * Save notes via AJAX
     */
    async saveNotes() {
        const notesTextarea = document.getElementById('course-notes');
        const saveBtn = document.getElementById('save-notes-btn');
        
        if (!notesTextarea || !saveBtn) return;
        
        const notes = notesTextarea.value;
        const cursoId = saveBtn.dataset.cursoId;
        
        // Show saving state
        const originalText = saveBtn.textContent;
        saveBtn.textContent = 'Salvando...';
        saveBtn.disabled = true;
        
        try {
            const response = await fetch(`/salvar_anotacoes/${cursoId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    anotacoes: notes
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.showNotification(result.message, 'success');
                saveBtn.textContent = '✓ Salvo';
                setTimeout(() => {
                    saveBtn.textContent = originalText;
                }, 2000);
            } else {
                this.showNotification(result.message || 'Erro ao salvar anotações', 'error');
                saveBtn.textContent = originalText;
            }
        } catch (error) {
            console.error('Error saving notes:', error);
            this.showNotification('Erro de conexão ao salvar anotações', 'error');
            saveBtn.textContent = originalText;
        } finally {
            saveBtn.disabled = false;
        }
    }

    /**
     * Auto-save notes (silent)
     */
    async autoSaveNotes() {
        const notesTextarea = document.getElementById('course-notes');
        const saveBtn = document.getElementById('save-notes-btn');
        
        if (!notesTextarea || !saveBtn) return;
        
        const notes = notesTextarea.value;
        const cursoId = saveBtn.dataset.cursoId;
        
        try {
            const response = await fetch(`/salvar_anotacoes/${cursoId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    anotacoes: notes
                })
            });

            const result = await response.json();
            
            if (result.success) {
                // Show subtle auto-save indicator
                this.showAutoSaveIndicator();
            }
        } catch (error) {
            console.error('Error auto-saving notes:', error);
        }
    }

    /**
     * Show auto-save indicator
     */
    showAutoSaveIndicator() {
        const indicator = document.getElementById('auto-save-indicator');
        if (indicator) {
            indicator.style.opacity = '1';
            setTimeout(() => {
                indicator.style.opacity = '0';
            }, 2000);
        }
    }

    /**
     * Setup form enhancements
     */
    setupFormEnhancements() {
        // Add course form validation
        const addCourseForm = document.querySelector('form[action*="adicionar_curso"]');
        if (addCourseForm) {
            addCourseForm.addEventListener('submit', (e) => {
                if (!this.validateCourseForm(addCourseForm)) {
                    e.preventDefault();
                }
            });
        }
        
        // Delete confirmation enhancements
        const deleteButtons = document.querySelectorAll('form[action*="deletar_curso"] button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const form = button.closest('form');
                const courseTitle = button.closest('.course-card').querySelector('.course-title').textContent;
                
                this.showConfirmDialog(
                    'Confirmar Exclusão',
                    `Tem certeza que deseja deletar o curso "${courseTitle}"?`,
                    () => form.submit()
                );
            });
        });
    }

    /**
     * Validate course form
     */
    validateCourseForm(form) {
        const titulo = form.querySelector('#titulo').value.trim();
        const totalAulas = form.querySelector('#total_aulas').value.trim();
        
        if (!titulo) {
            this.showNotification('Título do curso é obrigatório', 'error');
            return false;
        }
        
        if (!totalAulas || isNaN(totalAulas) || parseInt(totalAulas) <= 0) {
            this.showNotification('Número total de aulas deve ser um número positivo', 'error');
            return false;
        }
        
        return true;
    }

    /**
     * Show confirmation dialog
     */
    showConfirmDialog(title, message, onConfirm) {
        const confirmed = confirm(`${title}\n\n${message}`);
        if (confirmed && onConfirm) {
            onConfirm();
        }
    }

    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `flash-message flash-${type}`;
        notification.textContent = message;
        
        // Find or create flash messages container
        let container = document.querySelector('.flash-messages');
        if (!container) {
            container = document.createElement('div');
            container.className = 'flash-messages';
            const main = document.querySelector('.container');
            main.insertBefore(container, main.firstChild);
        }
        
        // Add notification
        container.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    /**
     * Setup auto-hide for existing flash messages
     */
    setupFlashMessages() {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    if (message.parentNode) {
                        message.parentNode.removeChild(message);
                    }
                }, 300);
            }, 5000);
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WebCursosApp();
});

// Export for potential use in other scripts
window.WebCursosApp = WebCursosApp;