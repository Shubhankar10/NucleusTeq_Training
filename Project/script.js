// console.log("Script Running")
// document.addEventListener('DOMContentLoaded', function() {
//   fetch('/api/test')
//     .then(response => {
//       console.log(response)
//       if (!response.ok) {
//         throw new Error('Server not connected');
//       }
//       return response.json();
//     })
//     .then(data => {
//       const serverStatusMsg = document.getElementById('server-status-msg');
//       serverStatusMsg.textContent = 'Server connected';
      
//       // Server is connected, fetch and populate tables
//       fetch('/api/users')
//         .then(response => response.json())
//         .then(data => {
//           const usersTableBody = document.getElementById('users-table-body');
//           data.forEach(user => {
//             const row = document.createElement('tr');
//             row.innerHTML = `
//               <td>${user.UID}</td>
//               <td>${user.isAdmin}</td>
//               <td>${user.FullName}</td>
//               <td>${user.Email}</td>
//             `;
//             usersTableBody.appendChild(row);
//           });
//         })
//         .catch(error => console.error('Error fetching users:', error));

//       fetch('/api/items')
//         .then(response => response.json())
//         .then(data => {
//           const itemsTableBody = document.getElementById('items-table-body');
//           data.forEach(item => {
//             const row = document.createElement('tr');
//             row.innerHTML = `
//               <td>${item.SerialNumber}</td>
//               <td>${item.ItemName}</td>
//               <td>${item.Quantity}</td>
//               <td>${item.Category}</td>
//               <td>${item.AssignedTo}</td>
//             `;
//             itemsTableBody.appendChild(row);
//           });
//         })
//         .catch(error => console.error('Error fetching items:', error));
//     })
//     .catch(error => {
//       const serverStatusMsg = document.getElementById('server-status-msg');
//       serverStatusMsg.textContent = 'Server not connected';
//     });
// });


