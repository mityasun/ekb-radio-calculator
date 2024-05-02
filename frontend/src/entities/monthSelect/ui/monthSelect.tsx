import { useCallback, useEffect } from 'react';
import { useStore } from 'shared/store';
import { AdMonth, AppSelectOption } from 'shared/types';
import { AppSelect } from 'shared/ui/appSelect';
import { getMonthOptions } from 'shared/utils';
import { maxWidth } from '../configs';

export const MonthSelect = () => {
  const months = getMonthOptions('ru');
  const { appSettings, setMonth, clearCustomerSelections } = useStore();

  useEffect(() => {
    const defaultMonth = months.find((month: AdMonth) => month.default) || months[0];

    setMonth(defaultMonth);
  }, []);

  const options = months.map((month: AdMonth) => ({
    value: month.id.toString(),
    label: month.month
  }));

  const getValue = useCallback(() => {
    return appSettings.month
      ? options.find((month) => month.value.toString() === (appSettings.month?.id || '').toString())
      : null;
  }, [appSettings, options]);

  const onChange = (newValue: unknown) => {
    const selectedMonth = months.find((month) => month.id.toString() === (newValue as AppSelectOption).value);
    if (selectedMonth) {
      setMonth(selectedMonth);
      clearCustomerSelections();
    }
  };

  return <AppSelect maxWidth={maxWidth} options={options} onChange={onChange} value={getValue()} />;
};
