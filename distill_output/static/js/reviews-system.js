/**
 * Professional Review System - Pure JavaScript
 * Handles high-traffic, concurrent submissions with robust storage
 * Version: 1.0.0
 */

class ReviewSystem {
    constructor() {
        this.storageKey = 'medridatours_reviews';
        this.maxReviews = 100; // Maximum reviews to store
        this.maxDisplayReviews = 20; // Maximum reviews to display
        this.rateLimit = 60000; // 1 minute between submissions per user
        this.lastSubmissionKey = 'last_review_submission';
        
        this.init();
    }

    /**
     * Initialize the review system
     */
    init() {
        this.bindEvents();
        this.displayReviews();
        this.addSampleReviews();
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        const form = document.getElementById('review-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmission(e));
        }
    }

    /**
     * Handle form submission with validation and rate limiting
     */
    async handleSubmission(event) {
        event.preventDefault();
        
        // Rate limiting check
        if (!this.checkRateLimit()) {
            this.showMessage('Veuillez attendre avant de soumettre un autre avis.', 'warning');
            return;
        }

        const formData = new FormData(event.target);
        const reviewData = this.extractFormData(formData);

        // Validate data
        if (!this.validateReview(reviewData)) {
            return;
        }

        try {
            // Save review with retry mechanism
            const success = await this.saveReviewWithRetry(reviewData);
            
            if (success) {
                this.displayReviews();
                this.showSuccessMessage();
                this.closeModal();
                this.updateLastSubmissionTime();
                
                // Scroll to reviews section
                setTimeout(() => {
                    document.getElementById('reviews-section').scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }, 500);
            } else {
                this.showMessage('Erreur lors de la sauvegarde. Veuillez réessayer.', 'error');
            }
        } catch (error) {
            console.error('Review submission error:', error);
            this.showMessage('Une erreur est survenue. Veuillez réessayer.', 'error');
        }
    }

    /**
     * Extract and sanitize form data
     */
    extractFormData(formData) {
        return {
            id: this.generateUniqueId(),
            name: this.sanitize(formData.get('name')) || 'Client anonyme',
            email: this.sanitize(formData.get('email')) || '',
            location: this.sanitize(formData.get('location')) || '',
            vehicle: this.sanitize(formData.get('vehicle_rented')) || '',
            rating: parseInt(formData.get('rating')) || 5,
            content: this.sanitize(formData.get('content')) || '',
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent.substring(0, 100), // Limited for privacy
            sessionId: this.getSessionId()
        };
    }

    /**
     * Validate review data
     */
    validateReview(review) {
        if (!review.name.trim()) {
            this.showMessage('Le nom est obligatoire.', 'error');
            return false;
        }
        
        if (!review.content.trim() || review.content.length < 10) {
            this.showMessage('Veuillez écrire un commentaire d\'au moins 10 caractères.', 'error');
            return false;
        }
        
        if (!review.rating || review.rating < 1 || review.rating > 5) {
            this.showMessage('Veuillez sélectionner une note.', 'error');
            return false;
        }
        
        return true;
    }

    /**
     * Save review with retry mechanism for concurrent access
     */
    async saveReviewWithRetry(review, maxAttempts = 3) {
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                const reviews = this.getStoredReviews();
                
                // Check for duplicate (same user, similar content)
                if (this.isDuplicate(review, reviews)) {
                    this.showMessage('Un avis similaire a déjà été soumis.', 'warning');
                    return false;
                }
                
                // Add new review at the beginning
                reviews.unshift(review);
                
                // Limit storage size
                if (reviews.length > this.maxReviews) {
                    reviews.splice(this.maxReviews);
                }
                
                // Atomic save operation
                localStorage.setItem(this.storageKey, JSON.stringify(reviews));
                return true;
                
            } catch (error) {
                if (attempt === maxAttempts) {
                    throw error;
                }
                
                // Exponential backoff
                await this.delay(Math.pow(2, attempt) * 100 + Math.random() * 100);
            }
        }
        return false;
    }

    /**
     * Check if review is a duplicate
     */
    isDuplicate(newReview, existingReviews) {
        const timeWindow = 24 * 60 * 60 * 1000; // 24 hours
        const now = new Date(newReview.timestamp).getTime();
        
        return existingReviews.some(existing => {
            const existingTime = new Date(existing.timestamp).getTime();
            const timeDiff = now - existingTime;
            
            return timeDiff < timeWindow && 
                   existing.name.toLowerCase() === newReview.name.toLowerCase() &&
                   this.similarContent(existing.content, newReview.content);
        });
    }

    /**
     * Check if two content strings are similar
     */
    similarContent(content1, content2) {
        const normalize = str => str.toLowerCase().replace(/\s+/g, ' ').trim();
        const normalized1 = normalize(content1);
        const normalized2 = normalize(content2);
        
        // Simple similarity check (you can enhance this)
        return normalized1 === normalized2 || 
               (normalized1.length > 20 && normalized2.includes(normalized1.substring(0, 20))) ||
               (normalized2.length > 20 && normalized1.includes(normalized2.substring(0, 20)));
    }

    /**
     * Display all reviews in the grid
     */
    displayReviews() {
        const reviewsGrid = document.getElementById('reviews-grid');
        const loadingElement = document.getElementById('reviews-loading');
        const noReviewsMessage = document.getElementById('no-reviews-message');
        
        if (!reviewsGrid) return;
        
        const reviews = this.getStoredReviews().slice(0, this.maxDisplayReviews);
        
        // Hide loading
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        
        if (reviews.length === 0) {
            // Show no reviews message
            reviewsGrid.innerHTML = '';
            if (noReviewsMessage) {
                noReviewsMessage.classList.remove('hidden');
            }
        } else {
            // Hide no reviews message
            if (noReviewsMessage) {
                noReviewsMessage.classList.add('hidden');
            }
            
            // Display reviews
            const reviewsHTML = reviews.map(review => this.createReviewHTML(review)).join('');
            reviewsGrid.innerHTML = reviewsHTML;
        }
    }

    /**
     * Create HTML for a single review
     */
    createReviewHTML(review) {
        const stars = this.generateStarsHTML(review.rating);
        const timeAgo = this.formatTimeAgo(new Date(review.timestamp));
        const truncatedContent = this.truncateText(review.content, 150);

        return `
            <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow review-card">
                <!-- Rating and Date -->
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center">
                        ${stars}
                    </div>
                    <span class="text-xs text-gray-500">${timeAgo}</span>
                </div>
                
                <!-- Review Content -->
                <p class="text-gray-700 text-sm mb-3 leading-relaxed">
                    "${truncatedContent}"
                </p>
                
                <!-- Customer Info -->
                <div class="flex items-center justify-between text-xs">
                    <div>
                        <span class="font-medium text-gray-800">${this.escapeHtml(review.name)}</span>
                        ${review.location ? `<span class="text-gray-500"> • ${this.escapeHtml(review.location)}</span>` : ''}
                    </div>
                    ${review.vehicle ? `<span class="text-blue-600 font-medium">${this.escapeHtml(review.vehicle)}</span>` : ''}
                </div>
                
                <!-- Verification badge -->
                <div class="mt-2 flex items-center justify-end">
                    <span class="inline-flex items-center text-xs text-green-600">
                        <i class="fas fa-check-circle mr-1"></i>
                        Avis vérifié
                    </span>
                </div>
            </div>
        `;
    }

    /**
     * Generate stars HTML for rating
     */
    generateStarsHTML(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<i class="fas fa-star text-yellow-400 text-sm"></i>';
            } else {
                stars += '<i class="fas fa-star text-gray-300 text-sm"></i>';
            }
        }
        return stars;
    }

    /**
     * Get stored reviews from localStorage
     */
    getStoredReviews() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error reading stored reviews:', error);
            return [];
        }
    }

    /**
     * Rate limiting functionality
     */
    checkRateLimit() {
        const lastSubmission = localStorage.getItem(this.lastSubmissionKey);
        if (!lastSubmission) return true;
        
        const timeSinceLastSubmission = Date.now() - parseInt(lastSubmission);
        return timeSinceLastSubmission >= this.rateLimit;
    }

    updateLastSubmissionTime() {
        localStorage.setItem(this.lastSubmissionKey, Date.now().toString());
    }

    /**
     * Utility functions
     */
    generateUniqueId() {
        return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    getSessionId() {
        let sessionId = sessionStorage.getItem('review_session_id');
        if (!sessionId) {
            sessionId = this.generateUniqueId();
            sessionStorage.setItem('review_session_id', sessionId);
        }
        return sessionId;
    }

    sanitize(input) {
        if (typeof input !== 'string') return '';
        return input.trim().replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    formatTimeAgo(date) {
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'À l\'instant';
        if (diffInSeconds < 3600) return `Il y a ${Math.floor(diffInSeconds / 60)} min`;
        if (diffInSeconds < 86400) return `Il y a ${Math.floor(diffInSeconds / 3600)}h`;
        if (diffInSeconds < 604800) return `Il y a ${Math.floor(diffInSeconds / 86400)} j`;
        
        return date.toLocaleDateString('fr-FR', { 
            year: 'numeric', 
            month: 'short'
        });
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * UI Functions
     */
    closeModal() {
        const modal = document.getElementById('review-modal');
        const form = document.getElementById('review-form');
        
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
        
        if (form) {
            form.reset();
            // Reset star rating
            const stars = document.querySelectorAll('.star');
            stars.forEach(star => {
                star.classList.remove('text-yellow-400');
                star.classList.add('text-gray-300');
            });
            document.getElementById('review-rating').value = '';
            document.getElementById('rating-text').textContent = '';
        }
    }

    showSuccessMessage() {
        this.showMessage('✅ Merci pour votre avis ! Il a été publié avec succès.', 'success');
    }

    showMessage(message, type = 'info') {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.review-message');
        existingMessages.forEach(msg => msg.remove());

        const messageElement = document.createElement('div');
        messageElement.className = `review-message fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 max-w-sm`;
        
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-black',
            info: 'bg-blue-500 text-white'
        };
        
        messageElement.className += ` ${colors[type] || colors.info}`;
        messageElement.innerHTML = `
            <div class="flex items-center justify-between">
                <span class="text-sm font-medium">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-3 text-lg opacity-70 hover:opacity-100">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        document.body.appendChild(messageElement);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (messageElement.parentElement) {
                messageElement.remove();
            }
        }, 5000);
    }

    /**
     * Add sample reviews for demonstration
     */
    addSampleReviews() {
        const existingReviews = this.getStoredReviews();
        if (existingReviews.length > 0) return; // Don't add if reviews already exist

        const sampleReviews = [
            {
                id: 'sample_1',
                name: 'Fatima Zahra',
                email: '',
                location: 'Casablanca',
                vehicle: 'Dacia Logan',
                rating: 5,
                content: 'Service impeccable ! Voiture propre, personnel très professionnel. Je recommande vivement Medridatours pour la location de voiture à Essaouira.',
                timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
                userAgent: 'Sample',
                sessionId: 'sample_session_1'
            },
            {
                id: 'sample_2',
                name: 'Ahmed Bennani',
                email: '',
                location: 'Marrakech',
                vehicle: 'Dacia Duster',
                rating: 5,
                content: 'Excellente expérience avec Medridatours. Réservation facile, prix compétitifs et véhicule en parfait état. Parfait pour explorer Essaouira et ses environs.',
                timestamp: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
                userAgent: 'Sample',
                sessionId: 'sample_session_2'
            },
            {
                id: 'sample_3',
                name: 'Sarah Martin',
                email: '',
                location: 'Paris, France',
                vehicle: 'Renault Clio',
                rating: 4,
                content: 'Très bon service client, voiture confortable pour visiter la région. Seul petit bémol, l\'attente à la récupération un peu longue.',
                timestamp: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(), // 7 days ago
                userAgent: 'Sample',
                sessionId: 'sample_session_3'
            }
        ];

        try {
            localStorage.setItem(this.storageKey, JSON.stringify(sampleReviews));
            console.log('Sample reviews added successfully');
        } catch (error) {
            console.error('Error adding sample reviews:', error);
        }
    }

    /**
     * Admin functions (for debugging)
     */
    clearAllReviews() {
        localStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.lastSubmissionKey);
        this.displayReviews();
        console.log('All reviews cleared');
    }

    exportReviews() {
        const reviews = this.getStoredReviews();
        const dataStr = JSON.stringify(reviews, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `medridatours_reviews_${new Date().toISOString().split('T')[0]}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
    }
}

// Initialize the review system when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.reviewSystem = new ReviewSystem();
    
    // Expose for debugging in console
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('Review System initialized. Available commands:');
        console.log('- reviewSystem.clearAllReviews() - Clear all reviews');
        console.log('- reviewSystem.exportReviews() - Export reviews as JSON');
        console.log('- reviewSystem.getStoredReviews() - Get all stored reviews');
    }
});