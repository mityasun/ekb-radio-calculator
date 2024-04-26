import { useCallback, useEffect } from 'react';
import { useAdSettingsStore, useOrder } from 'shared/store';
import { AdMonth } from 'shared/types';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';
import { getMonthOptions } from 'shared/utils';

const maxWidth = '100%';

export const AdMonthSelector = () => {
  const months = getMonthOptions('ru');
  const { adSettings, setMonth } = useAdSettingsStore();
  const { clearCustomerSelections } = useOrder();

  useEffect(() => {
    const defaultMonth = months.find((month: AdMonth) => month.default) || months[0];

    setMonth(defaultMonth);
  }, []);

  const options = months.map((month: AdMonth) => ({
    value: month.id.toString(),
    label: month.month
  }));

  const getValue = useCallback(() => {
    return adSettings.month
      ? options.find((month) => month.value.toString() === (adSettings.month?.id || '').toString())
      : null;
  }, [adSettings, options]);

  const onChange = (newValue: unknown) => {
    const selectedMonth = months.find((month) => month.id.toString() === (newValue as AppSelectOption).value);
    if (selectedMonth) {
      setMonth(selectedMonth);
      clearCustomerSelections();
    }
  };

  return <AppSelect maxWidth={maxWidth} options={options} onChange={onChange} value={getValue()} />;
};
