const request = require('supertest');
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const bcrypt = require('bcrypt');
const app = require('./app'); // Import your Express app
const User = require('./models/users');

let mongoServer;

beforeAll(async () => {
  await mongoose.disconnect();
  mongoServer = await MongoMemoryServer.create();

  const mongoUri = await mongoServer.getUri();
  await mongoose.connect(mongoUri);
});

afterAll(async () => {
  await mongoose.connection.close();
  await mongoServer.stop();
});

describe('POST /users/connection', () => {
  let userEmail;
  let userPassword;
  let userToken;
  let userName;

  beforeEach(async () => {
    userName = 'Ranni';
    userEmail = 'ranni@mail.fr';
    userPassword = '123';
    userToken = '6lHCyi-6Vg8QDMhR3ZXBKlQNU070hQvS';

    const hashedPassword = bcrypt.hashSync(userPassword, 10);

    await User.create({
      email: userEmail,
      password: hashedPassword,
      token: userToken,
      username: userName,
    });
  });

  it('should return an error if the email is missing', async () => {
    const response = await request(app)
      .post('/users/connection')
      .send({
        password: userPassword,
      });

    expect(response.status).toBe(200);
    expect(response.body.result).toBe(false);
    expect(response.body.error).toBe('Missing or empty fields');
  });

});
