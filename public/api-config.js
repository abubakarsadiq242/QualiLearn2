/**
 * QualiLearn API Configuration
 * This file handles all API requests and authentication headers.
 */

// If running from a file or different port, point to the Flask server explicitly
const BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:')
    ? 'http://127.0.0.1:5000/api'
    : '/api';

// Helper to get headers with JWT token if available
function getHeaders() {
    const token = localStorage.getItem('ql_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}

// Global fetch wrapper
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: getHeaders()
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        console.log(`[API Request] ${method} ${BASE_URL}${endpoint}`, body || '');
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        
        let data;
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            data = await response.json();
        } else {
            // Received HTML/text instead of JSON (likely 404 or 500 error page)
            const text = await response.text();
            console.error(`[API Error] Received non-JSON response from ${endpoint}:`, text.substring(0, 200));
            throw new Error(`Server returned unexpected content type: ${contentType}. This usually means a 404 or 500 error.`);
        }
        
        console.log(`[API Response] ${endpoint}:`, data);
        
        if (!response.ok) {
            if (response.status === 401) {
                apiLogout();
            }
            throw new Error(data.message || 'Server error occurred');
        }
        
        return data;
    } catch (error) {
        console.error(`[API Error] (${endpoint}):`, error);
        // If it's a dashboard page, show a more user-friendly alert
        if (window.location.pathname.includes('dashboard')) {
            const alertBox = document.getElementById('auth-alert') || document.querySelector('.alert');
            if (alertBox) {
                alertBox.textContent = "Syncing with server failed. Please check your internet connection.";
                alertBox.classList.remove('d-none');
            }
        }
        throw error;
    }
}

// Authentication API
async function apiLogin(credentials) {
    const data = await apiCall('/auth/login', 'POST', credentials);
    if (data.success) {
        localStorage.setItem('ql_token', data.data.token);
        localStorage.setItem('ql_user', JSON.stringify(data.data.user));
        localStorage.setItem('ql_lang', data.data.user.language || 'en');
    }
    return data;
}

async function apiRegister(userData) {
    return await apiCall('/auth/register', 'POST', userData);
}

function apiLogout() {
    stopStudyTimer();
    localStorage.clear();
    window.location.href = 'login.html';
}

// User Profile API
async function apiGetProfile() {
    return await apiCall('/users/profile');
}

async function apiUpdateProfile(data) {
    return await apiCall('/users/profile/update', 'PUT', data);
}

// Dashboard API
async function apiGetDashboard() {
    const portal = getCurrentPortal();
    await flushAnalyticsQueue(); 
    return await apiCall(`/analytics/dashboard-stats?portal=${portal}`);
}

const apiUploadFile = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return fetch(`${BASE_URL}/learning/upload`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('ql_token')}`
        },
        body: formData
    }).then(res => res.json());
};

async function apiGetDashboardStats() {
    return await apiGetDashboard();
}

// Learning Materials API
async function apiGetMaterials(subject = '', lang = 'en', search = '') {
    return await apiCall(`/learning/materials?subject=${subject}&lang=${lang}&search=${search}`);
}

async function apiGetVocational(category = '', lang = 'en', search = '') {
    return await apiCall(`/learning/vocational?category=${category}&lang=${lang}&search=${search}`);
}

async function apiAdminDeleteMaterial(id) {
    return await apiCall(`/learning/materials/${id}`, 'DELETE');
}

async function apiGetMaterials() {
    return await apiCall('/learning/materials');
}

async function apiGetMaterial(id) {
    return await apiCall(`/learning/material/${id}`);
}

// Assessments API
async function apiGetPastQuestions(subject = '', year = '', lang = 'en') {
    return await apiCall(`/assessments/questions?subject=${subject}&year=${year}&lang=${lang}`);
}

async function apiStartAssessment(assessment_id) {
    return await apiCall('/assessments/start', 'POST', { assessment_id });
}



// Topic Management API
async function apiGetTopics() {
    return await apiCall('/topics/');
}

async function apiCreateTopic(name, subject) {
    return await apiCall('/topics/create', 'POST', { name, subject });
}

async function apiDeleteTopic(topicId) {
    return await apiCall(`/topics/delete/${topicId}`, 'POST');
}

async function apiAddTopicVideo(topicId, url, title = '') {
    return await apiCall(`/topics/${topicId}/add-video`, 'POST', { video_url: url, video_title: title });
}

async function apiGetTopicVideos(topicId) {
    return await apiCall(`/topics/${topicId}/videos`);
}

async function apiGetSubjectVideos(subject, level = '') {
    return await apiCall(`/topics/subject-videos?subject=${encodeURIComponent(subject)}&level=${level}`);
}

async function apiDeleteTopicVideo(videoId) {
    return await apiCall(`/videos/delete/${videoId}`, 'POST');
}

// Flashcards API
async function apiGetFlashcards(subject = '', lang = 'en') {
    return await apiCall(`/flashcards/?subject=${subject}&lang=${lang}`);
}

async function apiReviewFlashcard(card_id, correct) {
    return await apiCall(`/flashcards/${card_id}/review`, 'PATCH', { correct });
}

// Chat API
async function apiSendMessage(message) {
    return await apiCall('/chat/send', 'POST', { message });
}

async function apiGetChatHistory() {
    return await apiCall('/chat/history');
}

async function apiClearChatHistory() {
    return await apiCall('/chat/clear', 'DELETE');
}
async function apiCheckAnswer(question_id, answer) {
    return await apiCall('/assessments/check', 'POST', { question_id, answer });
}

// Admin Management API
async function apiAdminGetUsers() {
    return await apiCall('/users/');
}

async function apiAdminUpdateTopic(id, data) {
    return await apiCall(`/topics/update/${id}`, 'PUT', data);
}

async function apiAdminCreateMaterial(data) {
    return await apiCall('/learning/materials/create', 'POST', data);
}

async function apiAdminUpdateMaterial(id, data) {
    return await apiCall(`/learning/materials/${id}`, 'PUT', data);
}

async function apiAdminDeleteMaterial(id) {
    return await apiCall(`/learning/materials/${id}`, 'DELETE');
}

async function apiAdminCreateQuestion(data) {
    return await apiCall('/assessments/questions/create', 'POST', data);
}

async function apiAdminUpdateQuestion(id, data) {
    return await apiCall(`/assessments/questions/${id}`, 'PUT', data);
}

async function apiAdminDeleteQuestion(id) {
    return await apiCall(`/assessments/questions/${id}`, 'DELETE');
}

async function apiAdminCreateVocational(data) {
    return await apiCall('/learning/vocational/create', 'POST', data);
}

async function apiAdminUpdateVocational(id, data) {
    return await apiCall(`/learning/vocational/${id}`, 'PUT', data);
}

async function apiAdminDeleteVocational(id) {
    return await apiCall(`/learning/vocational/${id}`, 'DELETE');
}

async function apiAdminUpdateFlashcard(id, data) {
    return await apiCall(`/flashcards/${id}`, 'PUT', data);
}

async function apiAdminDeleteFlashcard(id) {
    return await apiCall(`/flashcards/${id}`, 'DELETE');
}

// Progress Tracking API
async function apiTrackProgress(topic_id, minutes = 5) {
    const portal_type = getCurrentPortal();
    const data = await apiCall('/learning/progress', 'POST', { topic_id, minutes, portal_type });
    if (data.success && data.data) {
        // Synchronize local storage user data
        localStorage.setItem('ql_user', JSON.stringify(data.data));
    }
    return data;
}
function getCurrentPortal() {
    const path = window.location.pathname.toLowerCase();
    if (path.includes('vocational')) return 'vocational';
    return 'secondary'; // Internally still 'secondary' for API compatibility
}

function getEmbedUrl(url) {
    if (!url) return '';
    if (url.includes('youtube-nocookie.com/embed/')) return url;
    
    // Robust YouTube ID extraction regex
    const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    const match = url.match(regex);
    const videoId = match ? match[1] : null;
    
    if (videoId) {
        return `https://www.youtube-nocookie.com/embed/${videoId}?rel=0&modestbranding=1&showinfo=0&autoplay=0&enablejsapi=1&origin=${window.location.origin}`;
    }
    
    return url;
}


async function apiStartSession() {
    const portal_type = getCurrentPortal();
    const res = await apiCall('/analytics/start-session', 'POST', { portal_type });
    if (res.success) {
        localStorage.setItem('ql_session_id', res.session_id);
        localStorage.setItem('ql_current_portal', portal_type);
    }
    return res;
}

async function apiEndSession() {
    const session_id = localStorage.getItem('ql_session_id');
    if (!session_id) return;
    return await apiCall('/analytics/end-session', 'POST', { session_id });
}

async function apiTrackActivity(data) {
    const session_id = localStorage.getItem('ql_session_id');
    const portal_type = getCurrentPortal();
    
    const payload = { 
        session_id, 
        portal_type,
        ...data,
        start_time: data.start_time || new Date().toISOString(),
        created_at: new Date().toISOString()
    };
    
    // Attempt immediate real-time sync
    try {
        const res = await apiCall('/analytics/batch-track', 'POST', { events: [payload] });
        if (res.success) return res;
    } catch (e) {}

    // Fallback to queue if offline
    const queue = JSON.parse(localStorage.getItem('ql_analytics_queue') || '[]');
    queue.push(payload);
    localStorage.setItem('ql_analytics_queue', JSON.stringify(queue));
    return { success: false, queued: true };
}

async function flushAnalyticsQueue() {
    const queue = JSON.parse(localStorage.getItem('ql_analytics_queue') || '[]');
    if (queue.length === 0) return { success: true };

    try {
        const response = await apiCall('/analytics/batch-track', 'POST', { events: queue });
        if (response.success) {
            localStorage.setItem('ql_analytics_queue', '[]');
            return response;
        }
    } catch (e) {
        console.warn("[Analytics] Sync failed, keeping in queue:", e.message);
    }
    return { success: false, queued: true };
}

// Analytics
async function apiGetSubjectProgress(subject) {
    const portal = getCurrentPortal();
    const lang = localStorage.getItem('ql_lang') || 'en';
    return await apiCall(`/analytics/subject-progress?subject=${subject}&portal=${portal}&lang=${lang}`);
}

async function apiGetLeaderboard() {
    const portal = getCurrentPortal();
    return await apiCall(`/analytics/leaderboard?portal=${portal}`);
}

// Global Study Session Tracker (Persistent)
let studyInterval = null;
let visualInterval = null;
let currentTopicId = null;
let lastActivityTime = Date.now();
const IDLE_THRESHOLD = 30 * 60 * 1000; // 30 minutes for long videos

// Track activity for idle detection
['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(evt => {
    window.addEventListener(evt, () => {
        lastActivityTime = Date.now();
    });
});

async function startStudyTimer(topic_id = null) {
    if (studyInterval) stopStudyTimer();
    
    // Ensure we have a session
    if (!localStorage.getItem('ql_session_id')) {
        await apiStartSession();
    }
    
    currentTopicId = topic_id || localStorage.getItem('ql_study_topic');
    if (topic_id) localStorage.setItem('ql_study_topic', topic_id);
    
    // Persist start time
    if (!localStorage.getItem('ql_study_start')) {
        localStorage.setItem('ql_study_start', Date.now());
        localStorage.setItem('ql_study_base_seconds', '0');
    }
    
    // Visual Timer Update
    const display = document.getElementById('studyTimerDisplay');
    updateVisuals();
    if (visualInterval) clearInterval(visualInterval);
    visualInterval = setInterval(updateVisuals, 1000);
    
    function updateVisuals() {
        const isIdle = (Date.now() - lastActivityTime) > IDLE_THRESHOLD;
        const isHidden = document.hidden;

        if (isIdle || isHidden) {
            if (display) display.style.opacity = '0.5';
            return;
        }
        if (display) display.style.opacity = '1';

        const start = parseInt(localStorage.getItem('ql_study_start') || Date.now());
        const base = parseInt(localStorage.getItem('ql_study_base_seconds') || 0);
        const elapsed = Math.floor((Date.now() - start) / 1000) + base;
        
        const mins = Math.floor(elapsed / 60);
        const secs = elapsed % 60;
        const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        
        if (display) display.textContent = timeStr;
    }
    
    // Throttled Sync
    const tabId = Math.random().toString(36).substring(7);
    
    // Only the visible tab can be the leader
    if (!document.hidden) localStorage.setItem('ql_clock_leader', tabId);

    if (studyInterval) clearInterval(studyInterval);
    // Increase frequency to 30 seconds for higher precision
    studyInterval = setInterval(async () => {
        if (localStorage.getItem('ql_clock_leader') !== tabId) return;
        
        // Idle or Hidden Check
        const isIdle = (Date.now() - lastActivityTime) > IDLE_THRESHOLD;
        const isHidden = document.hidden;
        
        if (isIdle || isHidden) return;

        try {
            await apiTrackActivity({
                activity_type: "study_session",
                module: localStorage.getItem('ql_study_topic_name') || "General",
                id: localStorage.getItem('ql_study_topic'),
                duration: 30, // Pulse every 30 seconds
                start_time: new Date(Date.now() - 30000).toISOString(),
                end_time: new Date().toISOString()
            });
            // Auto-refresh dash values if we are on the dashboard
            if (typeof refreshDashboardStats === 'function') refreshDashboardStats();
        } catch (e) { console.warn("[Analytics] Sync failed:", e); }
    }, 30000);

    // Heartbeat for leader election - only if visible
    setInterval(() => {
        if (!document.hidden) {
            localStorage.setItem('ql_clock_leader', tabId);
        }
    }, 5000);
}

function stopStudyTimer(clear = false) {
    if (studyInterval) { clearInterval(studyInterval); studyInterval = null; }
    if (visualInterval) { clearInterval(visualInterval); visualInterval = null; }
    
    if (clear) {
        apiEndSession();
        localStorage.removeItem('ql_session_id');
        localStorage.removeItem('ql_study_start');
        localStorage.removeItem('ql_study_base_seconds');
        localStorage.removeItem('ql_study_topic');
    } else {
        const start = parseInt(localStorage.getItem('ql_study_start') || Date.now());
        const base = parseInt(localStorage.getItem('ql_study_base_seconds') || 0);
        const elapsed = Math.floor((Date.now() - start) / 1000) + base;
        localStorage.setItem('ql_study_base_seconds', elapsed.toString());
        localStorage.removeItem('ql_study_start');
    }
}

// Auto-resume if in a session
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('ql_study_start') || localStorage.getItem('ql_study_base_seconds')) {
        const studyPages = ['learning.html', 'flashcard.html', 'assessment.html'];
        if (studyPages.some(p => window.location.pathname.endsWith(p))) {
            startStudyTimer();
        }
    }
});

async function apiSubmitAssessment(assessment_id, answers) {
    const portal_type = getCurrentPortal();
    const data = await apiCall('/assessments/submit', 'POST', { assessment_id, answers, portal_type });
    if (data.success && data.data) {
        // Update local user data with new stats
        const user = JSON.parse(localStorage.getItem('ql_user') || '{}');
        if (data.data.passed) {
            user.assessments_passed = (user.assessments_passed || 0) + 1;
        }
        // Increment study time slightly for the assessment session (e.g. 5 mins)
        user.study_time = (user.study_time || 0) + 5; 
        localStorage.setItem('ql_user', JSON.stringify(user));
        
        // Trigger dashboard refresh if active
        if (typeof refreshDashboardStats === 'function') refreshDashboardStats();
    }
    return data;
}

// Ensure timer stops when user leaves or closes tab
window.addEventListener('beforeunload', stopStudyTimer);

/**
 * Access Control Utility
 * Hides vocational features if the user is in the Secondary school portal
 */
function checkAccessControl() {
    const userStr = localStorage.getItem('ql_user');
    if (!userStr) return;
    
    const user = JSON.parse(userStr);
    const currentPage = window.location.pathname.split('/').pop().toLowerCase();
    
    // Portal definition
    const vocationalPages = ['vocational.html', 'vocational-dashboard.html', 'vocational-chat.html', 'vocational-profile.html'];
    const academicPages = ['dashboard.html', 'learning.html', 'assessment.html', 'flashcard.html', 'games.html', 'chat.html', 'profile.html'];
    const adminPages = ['admin.html', 'admin-curriculum.html', 'admin-content.html', 'admin-assessments.html', 'admin-vocational.html'];

    // Prevent students from accessing admin pages
    if (user.role !== 'admin' && adminPages.includes(currentPage)) {
        window.location.href = 'dashboard.html';
        return;
    }

    const academicLevels = ['Academics'];
    
    if (academicLevels.includes(user.education_level)) {
        // ACADEMIC USER: Prevent access to vocational pages
        if (vocationalPages.includes(currentPage)) {
            window.location.href = 'dashboard.html';
            return;
        }

        // Hide vocational entry points in academic portal
        const vocLinks = document.querySelectorAll('a[href*="vocational"]');
        vocLinks.forEach(link => {
            const parent = link.closest('.nav-link') || link;
            parent.style.display = 'none';
        });
    } else if (user.education_level === 'Vocational') {
        // VOCATIONAL USER: Prevent access to academic pages
        if (academicPages.includes(currentPage)) {
            window.location.href = 'vocational-dashboard.html';
            return;
        }

        // Hide academic entry points if any left (though we cleaned templates)
        const academicLinks = document.querySelectorAll('a[href="learning.html"], a[href="assessment.html"], a[href="flashcard.html"], a[href="games.html"]');
        academicLinks.forEach(link => {
            const parent = link.closest('.nav-link') || link;
            parent.style.display = 'none';
        });
    }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
    checkAccessControl();
    redirectByLevel();
});

/**
 * Redirects the user to the appropriate dashboard based on their education level
 */
function redirectByLevel() {
    const userStr = localStorage.getItem('ql_user');
    if (!userStr) return;
    
    const user = JSON.parse(userStr);
    const currentPage = window.location.pathname.split('/').pop().toLowerCase() || 'index.html';
    
    if (user.role === 'admin') {
        if (['index.html', 'login.html', 'dashboard.html', ''].includes(currentPage)) {
            window.location.href = 'admin.html';
        }
        return;
    }

     if (user.education_level === 'Vocational') {
        // Vocational students go to the Skill Hub
        if (['dashboard.html', 'index.html', 'login.html', ''].includes(currentPage)) {
            window.location.href = 'vocational-dashboard.html';
        }
    } else {
         // Academic students (JSS/SSS)
         if (['vocational-dashboard.html', 'vocational.html', 'login.html', 'index.html', ''].includes(currentPage) && localStorage.getItem('ql_token')) {
             window.location.href = 'dashboard.html';
         }
    }
}

// Global logo click handler
document.addEventListener('click', (e) => {
    const brand = e.target.closest('.navbar-brand');
    if (brand) {
        const userStr = localStorage.getItem('ql_user');
        if (userStr) {
            e.preventDefault();
            const user = JSON.parse(userStr);
            if (user.role === 'admin') window.location.href = 'admin.html';
            else if (user.education_level === 'Vocational') window.location.href = 'vocational-dashboard.html';
            else window.location.href = 'dashboard.html';
        }
    }
});
