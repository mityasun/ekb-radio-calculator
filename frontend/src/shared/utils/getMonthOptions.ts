export const getMonthOptions = (lang: string) => {
  const result = [];
  const date = new Date();

  for (let i = 0; i < 12; i++) {
    const monthDate = new Date(date.getFullYear(), date.getMonth() + i);
    const id = Number(monthDate.toLocaleString(lang, { month: 'numeric' }));
    const month = monthDate.toLocaleString(lang, { month: 'long' });
    const label = month.charAt(0).toUpperCase() + month.slice(1);
    const defaultMonth = date.getMonth() + 1 === id;

    result.push({ id, month: label, default: defaultMonth });
  }

  return result;
};
