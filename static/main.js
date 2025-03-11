document.addEventListener('DOMContentLoaded', function() {
    // จัดการปุ่มลบ (Delete)
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        const itemId = this.getAttribute('data-id');
        // ให้ผู้ใช้กรอกรหัสยืนยัน (ตัวอย่างใช้ "1234")
        const userCode = prompt("กรุณากรอกรหัสยืนยันเพื่อลบรายการนี้:");
        if (userCode === "1234") {
          fetch(`/delete/${itemId}`, {
            method: 'POST',
            headers: {
              'X-Requested-With': 'XMLHttpRequest'
            }
          })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              const itemElement = document.getElementById(`item-${itemId}`);
              if (itemElement) {
                itemElement.remove();
              }
              showNotification('ลบรายการสำเร็จ');
            } else {
              showNotification('เกิดข้อผิดพลาดในการลบรายการ');
            }
          })
          .catch(error => {
            console.error('Error:', error);
            showNotification('เกิดข้อผิดพลาดในการลบรายการ');
          });
        } else {
          showNotification('รหัสไม่ถูกต้อง');
        }
      });
    });
  
    // จัดการฟอร์มแก้ไข (Update)
    const updateForms = document.querySelectorAll('.update-form');
    updateForms.forEach(form => {
      form.addEventListener('submit', function(event) {
        // ให้ผู้ใช้กรอกรหัสยืนยันสำหรับการแก้ไข
        const password = prompt("กรุณากรอกรหัสยืนยันเพื่อแก้ไขรายการ:");
        if (password !== "1234") {
          event.preventDefault();
          showNotification("รหัสไม่ถูกต้องสำหรับการแก้ไข");
        }
      });
    });
  });
  
  // ฟังก์ชันสำหรับแสดงข้อความแจ้งเตือน
  function showNotification(message) {
    const notification = document.getElementById('notification');
    notification.style.display = 'block';
    notification.textContent = message;
    // ซ่อนข้อความหลังจาก 3 วินาที
    setTimeout(() => {
      notification.style.display = 'none';
      notification.textContent = '';
    }, 3000);
  }
  