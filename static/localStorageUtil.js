// Function to store user ID in localStorage
function storeUserId(userId) {
    localStorage.setItem("user_id", userId);
    console.log("User ID stored in localStorage:", userId);
}

// Function to remove user ID from localStorage
function removeUserId() {
    localStorage.removeItem("user_id");
    console.log("User ID removed from localStorage");
}

// Function to retrieve user ID from localStorage
function getUserId() {
    return localStorage.getItem("user_id");
}

