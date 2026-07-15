function titleFor(name) { return `Hello, ${name}`; }
if (typeof Page === 'function') Page({ data: { title: titleFor('Agent') } });
module.exports = { titleFor };
