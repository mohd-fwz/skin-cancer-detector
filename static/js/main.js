// ============================================
// DermaDetectAI - Main JavaScript
// ============================================

// Initialize Swiper when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Image Slider
    const swiper = new Swiper('.exampleSwiper', {
        loop: true,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        effect: 'slide',
        speed: 600,
    });
    
    // File Upload Handling
    const uploadArea = document.getElementById('uploadArea');
    const imageInput = document.getElementById('imageInput');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const uploadPreview = document.getElementById('uploadPreview');
    const previewImage = document.getElementById('previewImage');
    const removeImageBtn = document.getElementById('removeImage');
    
    let uploadedFile = null;
    
    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target !== removeImageBtn && !removeImageBtn.contains(e.target)) {
            imageInput.click();
        }
    });
    
    // File selection
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFileUpload(file);
        } else {
            alert('Please upload an image file (JPG, PNG)');
        }
    });
    
    // Remove image
    removeImageBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        uploadedFile = null;
        imageInput.value = '';
        uploadPlaceholder.style.display = 'block';
        uploadPreview.style.display = 'none';
    });
    
    // Handle file upload
    function handleFileUpload(file) {
        // Check file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB');
            return;
        }
        
        // Check file type
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }
        
        uploadedFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            uploadPlaceholder.style.display = 'none';
            uploadPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
    
    // Form Submission
    const analysisForm = document.getElementById('analysisForm');
    const startAnalysisBtn = document.getElementById('startAnalysisBtn');
    const resultsSection = document.getElementById('resultsSection');
    const skeletonLoader = document.getElementById('skeletonLoader');
    const actualResults = document.getElementById('actualResults');
    
    analysisForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate image upload
        if (!uploadedFile) {
            alert('Please upload an image before starting analysis');
            return;
        }
        
        // Get form data
        const formData = new FormData();
        formData.append('file', uploadedFile);
        formData.append('age', document.getElementById('age').value);
        formData.append('gender', document.getElementById('gender').value);
        formData.append('skinType', document.getElementById('skinType').value);
        formData.append('location', document.getElementById('location').value);
        formData.append('lesionSize', document.getElementById('lesionSize').value);
        formData.append('duration', document.getElementById('duration').value);
        formData.append('familyHistory', document.getElementById('familyHistory').value);
        formData.append('sunExposure', document.getElementById('sunExposure').value);
        
        // Get symptoms
        const symptoms = [];
        document.querySelectorAll('.symptoms-checkbox input[type="checkbox"]:checked').forEach(cb => {
            symptoms.push(cb.value);
        });
        formData.append('symptoms', JSON.stringify(symptoms));
        formData.append('additionalNotes', document.getElementById('additionalNotes').value);
        
        // Disable button and show loading
        startAnalysisBtn.disabled = true;
        startAnalysisBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
        
        // Show results section with skeleton loader
        resultsSection.style.display = 'block';
        skeletonLoader.style.display = 'block';
        actualResults.style.display = 'none';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        try {
            // Upload image first
            const uploadResponse = await axios.post('/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            if (uploadResponse.data.success) {
                // Simulate analysis delay (remove this when connecting real model)
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Get prediction
                const predictResponse = await axios.post('/predict', formData);
                
                // Display results
                displayResults(predictResponse.data);
            }
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis. Please try again.');
            resultsSection.style.display = 'none';
        } finally {
            // Re-enable button
            startAnalysisBtn.disabled = false;
            startAnalysisBtn.innerHTML = '<i class="bi bi-cpu-fill me-2"></i>Start AI Analysis';
        }
    });
    
    // Display Results Function
    function displayResults(data) {
        // Hide skeleton, show results
        skeletonLoader.style.display = 'none';
        actualResults.style.display = 'block';
        
        // Set prediction type
        document.getElementById('predictionType').textContent = data.prediction || 'Unknown';
        
        // Set confidence with color
        const probability = (data.probability * 100).toFixed(1);
        const confidenceBar = document.getElementById('confidenceBar');
        const confidenceText = document.getElementById('confidenceText');
        const confidenceLabel = document.getElementById('confidenceLabel');
        
        // Animate progress bar
        setTimeout(() => {
            confidenceBar.style.width = probability + '%';
            confidenceText.textContent = probability + '%';
        }, 100);
        
        // Set color based on probability
        confidenceBar.classList.remove('bg-success', 'bg-warning', 'bg-danger');
        if (data.probability < 0.4) {
            confidenceBar.classList.add('bg-success');
            confidenceLabel.textContent = 'Low Risk';
            confidenceLabel.style.color = '#40916c';
        } else if (data.probability < 0.7) {
            confidenceBar.classList.add('bg-warning');
            confidenceLabel.textContent = 'Moderate';
            confidenceLabel.style.color = '#f77f00';
        } else {
            confidenceBar.classList.add('bg-danger');
            confidenceLabel.textContent = 'High Risk';
            confidenceLabel.style.color = '#d00000';
        }
        
        // Set AI explanation (will be replaced with real API call)
        const explanationBox = document.getElementById('aiExplanation');
        explanationBox.innerHTML = `
            <p>Based on the analysis of the dermoscopic image, the AI model has detected characteristics consistent with <strong>${data.prediction}</strong>.</p>
            <p>The model identified specific patterns and features in the lesion that suggest this classification with ${probability}% confidence.</p>
            <p><strong>Note:</strong> This is an automated analysis and should not replace professional medical examination.</p>
        `;
        
        // Set heatmap (placeholder for now)
        const heatmapImage = document.getElementById('heatmapImage');
        heatmapImage.src = data.heatmap || 'https://via.placeholder.com/400x400/008B8B/FFFFFF?text=Heatmap+Processing';
    }
    
});

// ============================================
// About Page - Cancer Type Selection
// ============================================

// Check if we're on the about page
if (document.querySelector('.cancer-type-btn')) {
    const cancerButtons = document.querySelectorAll('.cancer-type-btn');
    const cancerDetails = document.querySelectorAll('.cancer-detail-card');
    
    cancerButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cancerType = this.getAttribute('data-cancer');
            
            // Remove active class from all buttons
            cancerButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Hide all detail cards
            cancerDetails.forEach(card => card.classList.remove('active'));
            
            // Show selected detail card
            const selectedCard = document.getElementById(cancerType + '-detail');
            if (selectedCard) {
                selectedCard.classList.add('active');
                
                // Smooth scroll to details
                selectedCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    });
}