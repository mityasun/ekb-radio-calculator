import { FC, useEffect, useState } from 'react';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';
import { getMonthOptions } from 'shared/utils';

export interface AdMonthSelectorProps {
  onMonthChange: (month: string) => void;
}

const maxWidth = '100%';

const options = getMonthOptions('ru');

export const AdMonthSelector: FC<AdMonthSelectorProps> = ({ onMonthChange }) => {
  const [currentMonth, setCurrentMonth] = useState(options[0].value);

  const getValue = () => {
    return currentMonth ? options.find((m) => m.value === currentMonth) : '';
  };

  const onChange = (newValue: unknown) => {
    setCurrentMonth((newValue as AppSelectOption).value);
    onMonthChange((newValue as AppSelectOption).label);
  };

  useEffect(() => {
    onMonthChange(options.filter((d) => d.value === currentMonth)[0].label);
  }, []);

  return <AppSelect maxWidth={maxWidth} options={options} onChange={onChange} value={getValue()} />;
};
