// Local Reviews Storage and Display System
class LocalReviewsManager {
    constructor() {
        this.storageKey = 'medridatours_reviews';
        this.init();
    }

    init() {
        // Disabled automatic review display to avoid conflicts with Django testimonials
        // this.interceptFormSubmission();
        // this.displayStoredReviews();
    }

    // Intercept form submission to store review locally
    interceptFormSubmission() {
        document.addEventListener('DOMContentLoaded', () => {
            const form = document.querySelector('form[name="comments-home"]');
            if (!form) return;

            form.addEventListener('submit', (e) => {
                this.handleFormSubmission(e);
            });
        });
    }

    // Handle form submission
    handleFormSubmission(event) {
        const form = event.target;
        const formData = new FormData(form);
        
        // Extract form data
        const review = {
            id: Date.now() + Math.random().toString(36).substr(2, 9),
            name: formData.get('name') || 'Client anonyme',
            email: formData.get('email') || '',
            subject: formData.get('subject') || '',
            message: formData.get('message') || '',
            date: new Date().toISOString(),
            rating: 5, // Default rating
            approved: true // Auto-approve for local storage
        };

        // Validate required fields
        if (!review.name.trim() || !review.message.trim()) {
            return; // Let the form validation handle this
        }

        // Store the review
        this.storeReview(review);
        
        // Add small delay to show the review after form submission
        setTimeout(() => {
            this.displayStoredReviews();
            this.showSuccessMessage();
        }, 1000);
    }

    // Store review in localStorage
    storeReview(review) {
        let reviews = this.getStoredReviews();
        reviews.unshift(review); // Add to beginning
        
        // Keep only last 20 reviews to prevent storage bloat
        if (reviews.length > 20) {
            reviews = reviews.slice(0, 20);
        }
        
        localStorage.setItem(this.storageKey, JSON.stringify(reviews));
    }

    // Get stored reviews from localStorage
    getStoredReviews() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            return stored ? JSON.parse(stored) : [];
        } catch (e) {
            console.error('Error reading stored reviews:', e);
            return [];
        }
    }

    // Display stored reviews in the testimonials section
    displayStoredReviews() {
        const reviews = this.getStoredReviews();
        if (reviews.length === 0) return;

        // Find testimonials container
        const container = this.findTestimonialsContainer();
        if (!container) return;

        // Create reviews HTML
        const reviewsHTML = reviews.slice(0, 6).map(review => this.createReviewHTML(review)).join('');
        
        // Add or update reviews section
        this.updateTestimonialsSection(container, reviewsHTML);
    }

    // Find testimonials container
    findTestimonialsContainer() {
        // Look for testimonials section
        let container = document.getElementById('testimonials-section');
        if (!container) {
            container = document.querySelector('.testimonials');
        }
        if (!container) {
            container = document.querySelector('[id*="testimonial"]');
        }
        return container;
    }

    // Update testimonials section
    updateTestimonialsSection(container, reviewsHTML) {
        // Look for existing reviews grid
        let reviewsGrid = container.querySelector('#local-reviews-grid');
        
        if (!reviewsGrid) {
            // Create new reviews grid
            const existingGrid = container.querySelector('.grid');
            if (existingGrid) {
                // Add after existing testimonials
                reviewsGrid = document.createElement('div');
                reviewsGrid.id = 'local-reviews-grid';
                reviewsGrid.className = 'grid grid-cols-1 md:grid-cols-3 gap-6 mt-8';
                existingGrid.parentNode.insertBefore(reviewsGrid, existingGrid.nextSibling);
                
                // Add separator
                const separator = document.createElement('div');
                separator.className = 'border-t border-gray-200 my-8';
                existingGrid.parentNode.insertBefore(separator, reviewsGrid);
                
                // Add header
                const header = document.createElement('div');
                header.className = 'text-center mb-6';
                header.innerHTML = `
                    <h3 class="text-xl font-bold text-gray-800 mb-2">Avis Récents</h3>
                    <p class="text-gray-600">Les derniers retours de nos clients</p>
                `;
                reviewsGrid.parentNode.insertBefore(header, reviewsGrid);
            } else {
                // Create entire section if no grid exists
                const section = document.createElement('div');
                section.className = 'mt-8';
                section.innerHTML = `
                    <div class="text-center mb-6">
                        <h3 class="text-xl font-bold text-gray-800 mb-2">Avis Clients</h3>
                        <p class="text-gray-600">Les retours de nos clients</p>
                    </div>
                    <div id="local-reviews-grid" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
                `;
                container.appendChild(section);
                reviewsGrid = container.querySelector('#local-reviews-grid');
            }
        }
        
        reviewsGrid.innerHTML = reviewsHTML;
    }

    // Create HTML for a single review
    createReviewHTML(review) {
        const stars = this.generateStars(review.rating);
        const timeAgo = this.timeAgo(new Date(review.date));
        const truncatedMessage = review.message.length > 120 ? 
            review.message.substring(0, 120) + '...' : review.message;

        return `
            <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                <!-- Rating and Date -->
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center">
                        ${stars}
                    </div>
                    <span class="text-xs text-gray-500">${timeAgo}</span>
                </div>
                
                <!-- Review Content -->
                <p class="text-gray-700 text-sm mb-3 leading-relaxed">
                    "${truncatedMessage}"
                </p>
                
                <!-- Customer Info -->
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center text-gray-600">
                        <i class="fas fa-user-circle mr-1"></i>
                        <span class="font-medium">${review.name}</span>
                        ${review.subject ? `<span class="ml-2 text-gray-400">• ${review.subject}</span>` : ''}
                    </div>
                    <span class="text-blue-500 text-xs">
                        <i class="fas fa-check-circle mr-1"></i>Vérifié
                    </span>
                </div>
            </div>
        `;
    }

    // Generate star rating HTML
    generateStars(rating) {
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

    // Calculate time ago
    timeAgo(date) {
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
        const diffMinutes = Math.floor(diffTime / (1000 * 60));
        
        if (diffMinutes < 1) return 'À l\'instant';
        if (diffMinutes < 60) return `Il y a ${diffMinutes} min`;
        if (diffHours < 24) return `Il y a ${diffHours}h`;
        if (diffDays === 1) return 'Il y a 1 jour';
        if (diffDays < 7) return `Il y a ${diffDays} jours`;
        if (diffDays < 30) return `Il y a ${Math.floor(diffDays / 7)} semaine${Math.floor(diffDays / 7) > 1 ? 's' : ''}`;
        if (diffDays < 365) return `Il y a ${Math.floor(diffDays / 30)} mois`;
        return `Il y a ${Math.floor(diffDays / 365)} an${Math.floor(diffDays / 365) > 1 ? 's' : ''}`;
    }

    // Show success message
    showSuccessMessage() {
        // Create success notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-check-circle mr-2"></i>
                <span>Votre avis a été ajouté avec succès!</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 4 seconds
        setTimeout(() => {
            notification.remove();
        }, 4000);
        
        // Scroll to testimonials section
        const testimonialsSection = document.getElementById('testimonials-section');
        if (testimonialsSection) {
            setTimeout(() => {
                testimonialsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'center' 
                });
            }, 500);
        }
    }

    // Clear all stored reviews (for testing)
    clearAllReviews() {
        localStorage.removeItem(this.storageKey);
        this.displayStoredReviews();
        console.log('All reviews cleared');
    }

    // Add sample reviews (for demo)
    addSampleReviews() {
        const samples = [
            {
                id: 'sample1',
                name: 'Bizaline Jalila',
                message: 'Très belle expérience avec Medridatours, très bon service et véhicule en parfait état!',
                subject: 'Excellent service',
                date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
                rating: 5,
                approved: true
            },
            {
                id: 'sample2',
                name: 'Ahmed Benali',
                message: 'Location facile et rapide, personnel très accueillant. Je recommande vivement!',
                subject: 'Service rapide',
                date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
                rating: 5,
                approved: true
            }
        ];
        
        samples.forEach(sample => this.storeReview(sample));
        this.displayStoredReviews();
        console.log('Sample reviews added');
    }
}

// Initialize the reviews manager
const reviewsManager = new LocalReviewsManager();

// Expose for debugging in console
window.reviewsManager = reviewsManager;
