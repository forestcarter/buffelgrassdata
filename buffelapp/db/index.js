const pg = require('pg')

const pool = new pg.Pool({
    user: 'root',
    database: 'ndvidb',
    password: 'rootpass' 

});

module.exports = {
    query: (text, params, callback) => {
	return pool.query(text, params, callback)
    }
}
