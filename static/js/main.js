// Update range input values
function updateRangeValue(inputId, valueId) {
    const input = document.getElementById(inputId);
    const value = document.getElementById(valueId);
    value.textContent = input.value;
    input.addEventListener('input', (e) => {
        value.textContent = e.target.value;
    });
}

// Initialize range input displays
updateRangeValue('communication_skill', 'communication_value');
updateRangeValue('problem_solving_skill', 'problem_solving_value');
updateRangeValue('extracurriculars', 'extracurriculars_value');

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Predicting...';
    submitButton.disabled = true;
    
    try {
        const formData = new FormData(e.target);
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult(result);
        } else {
            throw new Error(result.error || 'Prediction failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        // Restore button state
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
});

// Display prediction results
function displayResult(result) {
    // Show result section
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';
    setTimeout(() => resultSection.classList.add('show'), 100);
    
    // Update prediction result
    const predictionResult = document.getElementById('predictionResult');
    predictionResult.textContent = `${result.name}: ${result.prediction}`;
    predictionResult.className = 'alert ' + 
        (result.prediction === 'Likely to be Placed' ? 'alert-success' : 'alert-warning');
    
    // Update probability bar
    const probabilityBar = document.getElementById('probabilityBar');
    probabilityBar.style.width = `${result.probability}%`;
    probabilityBar.textContent = `${result.probability}%`;
    
    // Update feature importance plot
    const featurePlot = document.getElementById('featurePlot');
    featurePlot.src = `data:image/png;base64,${result.plot}`;
    
    // Update suggestions
    const suggestionsList = document.getElementById('suggestions');
    suggestionsList.innerHTML = '';
    result.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
    
    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Load random sample data from the server
document.getElementById('sampleDataBtn').addEventListener('click', async () => {
    try {
        const response = await fetch('/sample-data');
        const samples = await response.json();
        
        // Randomly select one sample
        const sampleKeys = Object.keys(samples);
        const randomKey = sampleKeys[Math.floor(Math.random() * sampleKeys.length)];
        const sampleData = samples[randomKey];

        // Fill form with sample data
        document.getElementById('name').value = sampleData.name;
        document.getElementById('age').value = sampleData.age;
        document.getElementById('gender').value = sampleData.gender;
        document.getElementById('department').value = sampleData.department;
        document.getElementById('cgpa').value = sampleData.cgpa;
        document.getElementById('projects').value = sampleData.projects;
        document.getElementById('internships').value = sampleData.internships;
        document.getElementById('certifications').value = sampleData.certifications;
        document.getElementById('communication_skill').value = sampleData.communication;
        document.getElementById('problem_solving_skill').value = sampleData.problem_solving;
        document.getElementById('extracurriculars').value = sampleData.extracurriculars;

        // Update range value displays
        document.getElementById('communication_value').textContent = sampleData.communication;
        document.getElementById('problem_solving_value').textContent = sampleData.problem_solving;
        document.getElementById('extracurriculars_value').textContent = sampleData.extracurriculars;

        // Reset all checkboxes first
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => checkbox.checked = false);

        // Set the skills checkboxes
        sampleData.skills.forEach(skill => {
            const checkbox = document.getElementById(skill);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    } catch (error) {
        console.error('Error loading sample data:', error);
        alert('Error loading sample data');
    }
});

// Bind buttons to sample profiles
document.getElementById('sampleDataBtn1').addEventListener('click', () => loadSample(1));
document.getElementById('sampleDataBtn2').addEventListener('click', () => loadSample(2));
document.getElementById('sampleDataBtn3').addEventListener('click', () => loadSample(3));
