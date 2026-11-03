'use strict';
const http = require('node:http');
const net = require('node:net');
const fs = require('node:fs');
const path = require('node:path');
const port = Number(process.env.PORT || 3000);
const redisHost = process.env.REDIS_HOST;
let localVisits = 0;
const trips = [
  { id: 1, from: 'Улаанбаатар', to: 'Дархан', seats: 3, status: 'OPEN' },
  { id: 2, from: 'Улаанбаатар', to: 'Эрдэнэт', seats: 2, status: 'OPEN' },
  { id: 3, from: 'Дархан', to: 'Улаанбаатар', seats: 0, status: 'CLOSED' }
];
// Minimal Redis RESP request using Node's built-in TCP client. No npm dependencies.
function incrementRedis() {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection({ host: redisHost, port: Number(process.env.REDIS_PORT || 6379) });
    let buffer = '';
    let settled = false;
    const finish = (error, value) => {
      if (settled) return;
      settled = true;
      socket.destroy();
      error ? reject(error) : resolve(value);
    };
    socket.setTimeout(2000, () => finish(new Error('Redis timeout')));
    socket.on('error', err => finish(err));
    socket.on('connect', () => socket.write('*2\r\n$4\r\nINCR\r\n$14\r\nintercity:views\r\n'));
    socket.on('data', chunk => {
      buffer += chunk.toString('utf8');
      const end = buffer.indexOf('\r\n');
      if (end < 0) return;
      const reply = buffer.slice(0, end);
      if (/^:\d+$/.test(reply)) finish(null, Number(reply.slice(1)));
      else finish(new Error('Invalid Redis response'));
    });
    socket.on('end', () => { if (!settled) finish(new Error('Redis disconnected')); });
  });
}
function json(res, status, value) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(value));
}
const server = http.createServer(async (req, res) => {
  const pathname = new URL(req.url, 'http://localhost').pathname;
  console.log(`${new Date().toISOString()} ${req.method} ${pathname}`);
  if (req.method !== 'GET') return json(res, 405, { error: 'Method not allowed' });
  if (pathname === '/health') return json(res, 200, { status: 'ok', service: 'intercity-lab8' });
  if (pathname === '/api/trips') return json(res, 200, trips);
  if (pathname === '/api/visits') {
    try {
      const visits = redisHost ? await incrementRedis() : ++localVisits;
      return json(res, 200, { visits, storage: redisHost ? 'redis' : 'memory' });
    } catch (err) {
      console.error('Redis unavailable:', err.message);
      return json(res, 503, { error: 'Redis unavailable', storage: 'redis' });
    }
  }
  if (pathname !== '/') return json(res, 404, { error: 'Not found' });
  try {
    const html = fs.readFileSync(path.join(__dirname, 'public', 'index.html'));
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end(html);
  } catch (err) { json(res, 500, { error: 'Page could not be loaded' }); }
});
server.listen(port, '0.0.0.0', () => console.log(`Intercity Lab 8 listening on 0.0.0.0:${port}`));
process.on('SIGTERM', () => server.close(() => process.exit(0)));
