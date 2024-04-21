import { FC, useEffect, useState } from 'react';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';

export interface AdDurationSelectorProps {
  onDurationChange: (duration: string) => void;
}

const maxWidth = '100%';

const getDurationOptions = (startDuration: number, endDuration: number, period: number): AppSelectOption[] => {
  const result: AppSelectOption[] = [];

  for (let i = startDuration; i <= endDuration; i += period) {
    result.push({
      value: i.toString(),
      label: `${i.toString()} сек`
    });
  }

  return result;
};

const options = getDurationOptions(5, 30, 5);

export const AdDurationSelector: FC<AdDurationSelectorProps> = ({ onDurationChange }) => {
  const [currentDuration, setCurrentDuration] = useState(options[0].value);

  useEffect(() => {
    onDurationChange(currentDuration);
  }, []);

  const getValue = () => {
    return currentDuration ? options.find((d) => d.value === currentDuration) : '';
  };

  const onChange = (newValue: unknown) => {
    setCurrentDuration((newValue as AppSelectOption).value);
    onDurationChange((newValue as AppSelectOption).value);
  };

  return <AppSelect maxWidth={maxWidth} options={options} onChange={onChange} value={getValue()} />;
};
