import { formatPrice } from '../src/money/format';
test('whole numbers keep two decimals', () => {
  expect(formatPrice(1200, '$')).toBe('$12.00');
});
