import { AppSelectOption } from 'shared/ui/appSelect';

export const getMonthOptions = (lang: string): AppSelectOption[] => {
  const result: AppSelectOption[] = [];
  const date = new Date();

  for (let i = 0; i < 12; i++) {
    const monthDate = new Date(date.getFullYear(), date.getMonth() + i);
    const value = monthDate.toLocaleString(lang, { dateStyle: 'short' });
    const month = monthDate.toLocaleString(lang, { month: 'long' });
    const label = month.charAt(0).toUpperCase() + month.slice(1);

    result.push({ value, label });
  }

  return result;
};
