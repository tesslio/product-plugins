import { legacyHeader } from '../src/export/legacy';
test('legacy header uses commas', () => {
  expect(legacyHeader()).toBe('sku,qty,price');
});
