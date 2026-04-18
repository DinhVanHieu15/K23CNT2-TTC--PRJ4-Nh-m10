// // MỞ MODAL
// function openModal(type = "login") {
//     document.getElementById("authModal").style.display = "flex";
//     switchTab(type);
// }

// // ĐÓNG MODAL
// function closeModal() {
//     document.getElementById("authModal").style.display = "none";
// }

// // CHUYỂN TAB
// function switchTab(type) {
//     document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
//     document.querySelectorAll(".form").forEach(f => f.classList.remove("active"));

//     if (type === "login") {
//         document.querySelectorAll(".tab")[0].classList.add("active");
//         document.getElementById("loginForm").classList.add("active");
//     } else {
//         document.querySelectorAll(".tab")[1].classList.add("active");
//         document.getElementById("registerForm").classList.add("active");
//     }
// }

// // CLICK RA NGOÀI ĐỂ TẮT
// window.onclick = function(e) {
//     let modal = document.getElementById("authModal");
//     if (e.target === modal) {
//         modal.style.display = "none";
//     }
// }

// ================= REGISTER =================
function handleRegister() {
    alert("Đăng ký thành công!");

    // chuyển sang trang login
    window.location.href = "login.html";
}

// ================= LOGIN =================
function handleLogin() {
    alert("Đăng nhập thành công!");

    // chuyển sang trang sản phẩm (sau này là dashboard)
    window.location.href = "../home/index.html";
}
