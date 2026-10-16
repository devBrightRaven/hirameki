/** Package task readers from canonical sources; no installer or runtime writes. */
import { copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const dependencies = [
  'task_view.py', 'task_view_cli.py', 'archive_gate.py',
  'task_contract_primitives.py', 'TASK_GATE_VERSION', 'tidy_dry_run.py',
  'task_restore_contract.py',
];

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = join(root, 'scripts');
const skill = join(root, 'codex', 'skills', 'hirameki');
const destination = join(skill, 'scripts');

for (const directory of [source, join(root, 'codex'), join(root, 'codex', 'skills'), skill]) {
  if (!lstatSync(directory).isDirectory() || lstatSync(directory).isSymbolicLink()) {
    throw new Error(`Invalid package source directory: ${directory}`);
  }
}
for (const name of dependencies) {
  const origin = join(source, name);
  if (!lstatSync(origin).isFile() || lstatSync(origin).isSymbolicLink()) {
    throw new Error(`Missing or linked package dependency: ${name}`);
  }
}
if (existsSync(destination)) {
  if (!lstatSync(destination).isDirectory() || lstatSync(destination).isSymbolicLink()) {
    throw new Error('Package script destination must be a real directory');
  }
  if (readdirSync(destination).some(name => !dependencies.includes(name))) {
    throw new Error('Preserve unexpected existing package script files');
  }
  for (const name of dependencies) {
    const target = join(destination, name);
    if (existsSync(target) && (lstatSync(target).isSymbolicLink()
      || !lstatSync(target).isFile()
      || !readFileSync(target).equals(readFileSync(join(source, name))))) {
      throw new Error(`Preserve divergent existing package dependency: ${name}`);
    }
  }
}
mkdirSync(destination, { recursive: true });
for (const name of dependencies) {
  const target = join(destination, name);
  if (!existsSync(target)) copyFileSync(join(source, name), target);
}
console.log(`Packaged ${dependencies.length} task dependencies under codex/skills/hirameki/scripts`);
