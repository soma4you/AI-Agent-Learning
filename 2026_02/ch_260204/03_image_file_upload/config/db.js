const { MongoClient } = require('mongodb');

const url = 'mongodb://localhost:27017';
const dbName = 'kosta285';
let dbInstance = null;

const connectDB = async () => {
    if (dbInstance) return dbInstance;
    try {
        const client = new MongoClient(url);
        await client.connect();
        console.log('MongoDB(Native) Connected successfully to server');
        dbInstance = client.db(dbName);
        return dbInstance;
    } catch (err) {
        console.error('MongoDB connection error:', err);
        process.exit(1);
    }
};

const getDb = () => {
    if (!dbInstance) {
        throw new Error('Database not initialized. Call connectDB first.');
    }
    return dbInstance;
};

module.exports = { connectDB, getDb };