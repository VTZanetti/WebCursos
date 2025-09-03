const axios = require('axios');

async function testCreateCourse() {
  try {
    const response = await axios.post('http://localhost:5000/api/cursos', {
      titulo: 'Test Course',
      total_aulas: 10
    });
    console.log('Response status:', response.status);
    console.log('Response data:', JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
  }
}

testCreateCourse();