import { useState } from 'react';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';

const options: AppSelectOption[] = [
  {
    value: 'europa_plus',
    label: 'Европа Плюс'
  },
  {
    value: 'radio_CI',
    label: 'Радио СИ'
  },
  {
    value: 'autoradio',
    label: 'Авторадио'
  }
];

export const RadioStationSelect = () => {
  const [currentRadioStation, setCurrentRadioStation] = useState('autoradio');

  const getValue = () => {
    return currentRadioStation ? options.find((station) => station.value === currentRadioStation) : '';
  };

  const onChange = (newValue: unknown) => {
    setCurrentRadioStation((newValue as AppSelectOption).value);
  };

  return <AppSelect maxWidth={'275px'} options={options} onChange={onChange} value={getValue()} />;
};
