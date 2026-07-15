const test = require('node:test');
const assert = require('node:assert/strict');
const { titleFor } = require('../miniprogram/pages/index/index');
test('builds a display title', () => assert.equal(titleFor('Agent'), 'Hello, Agent'));
