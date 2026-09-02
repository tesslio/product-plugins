export function parseRows(text: string): string[][] {
  return text.split('\n').filter((line) => line.length > 0).map((line) => line.split(','));
}
