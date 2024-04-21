import { FC, useEffect, useState } from 'react';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';

export interface AdPositionSelectorProps {
  onPositionChange: (position: string) => void;
}

const maxWidth = '100%';

const options: AppSelectOption[] = [
  {
    value: 'bez-pozicionirovaniya',
    label: 'Без позиционирования'
  },
  {
    value: 'perviy-v-reklamnom-bloke',
    label: 'Первый в рекламном блоке'
  },
  {
    value: 'posledniy-v-reklamnom-bloke',
    label: 'Последний в рекламном блоке'
  }
];

export const AdPositionSelector: FC<AdPositionSelectorProps> = ({ onPositionChange }) => {
  const [currentPosition, setCurrentPosition] = useState(options[0].value);

  const getValue = () => {
    return currentPosition ? options.find((d) => d.value === currentPosition) : '';
  };

  const onChange = (newValue: unknown) => {
    setCurrentPosition((newValue as AppSelectOption).value);
    onPositionChange((newValue as AppSelectOption).value);
  };

  useEffect(() => {
    onPositionChange(currentPosition);
  }, []);

  return <AppSelect maxWidth={maxWidth} options={options} onChange={onChange} value={getValue()} />;
};
