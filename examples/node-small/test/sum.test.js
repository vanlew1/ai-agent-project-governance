const test = require('node:test');
const assert = require('node:assert/strict');
const { sum } = require('../src/sum');
test('adds two numbers', () => assert.equal(sum(2, 3), 5));
