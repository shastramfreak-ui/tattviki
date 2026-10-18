#!/usr/bin/env node
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync('assets/content.js', 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync('assets/curriculum.js', 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync('assets/enterprise_curriculum.js', 'utf8'), sandbox);
vm.runInNewContext(fs.readFileSync('assets/enterprise_cases.js', 'utf8'), sandbox);
const { paths, lessons, tools, methods, glossary, challenges } = sandbox.window.OT;
function unique(xs, category) {
  const set = new Set(xs);
  assert.equal(set.size, xs.length, `Duplicate ${category}`);
}
unique(paths.map(x => x.id), 'learning path ID');
unique(lessons.map(x => x.id), 'lesson ID');
unique(lessons.map(x => x.title.toLocaleLowerCase().trim()), 'lesson title');
assert.equal(lessons.length, 613, 'Expected 613 lessons');
assert.equal(sandbox.window.TATTVIKI_ENTERPRISE_CASES.length, 12, 'Expected 12 enterprise blueprints');
unique(tools.map(x => x.name.toLowerCase()), 'tool');
unique(glossary.map(([term]) => term.toLowerCase()), 'glossary term');
assert(lessons.length >= 250);
for (const lesson of lessons) {
  assert(paths.some(p => p.id === lesson.path), `Unknown lesson path ${lesson.id}`);
  for (const key of ['title','description','analogy','example','try','resource','quiz'])
    assert(lesson[key], `Missing ${key} in ${lesson.id}`);
  assert(Array.isArray(lesson.learn) && lesson.learn.length >= 2, `Missing objectives in ${lesson.id}`);
  assert(lesson.quiz.options.length === 3 && lesson.quiz.answer >= 0 && lesson.quiz.answer < 3,
    `Invalid quiz in ${lesson.id}`);
  assert(/^https:\/\//.test(lesson.resource.url), `Unsafe reference in ${lesson.id}`);
}
for (const tool of tools) assert(/^https:\/\//.test(tool.url), `Non-HTTPS tool: ${tool.name}`);
for (const method of methods) assert(/^https?:\/\//.test(method.url), `Invalid methodology URL: ${method.name}`);
for (const challenge of challenges) assert(challenge.solution.includes('SELECT'), `Invalid challenge: ${challenge.title}`);
const updates = JSON.parse(fs.readFileSync('data/updates.json', 'utf8'));
for (const u of updates.items) assert(/^https:\/\//.test(u.url), `Unsafe news URL ${u.title}`);
console.log(`Validated ${lessons.length} lessons, ${tools.length} tools, ${methods.length} methods, ${updates.items.length} news sources.`);
