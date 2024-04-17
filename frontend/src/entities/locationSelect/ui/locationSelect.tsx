import { useState } from 'react';
import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';

const options: AppSelectOption[] = [
  {
    value: 'moscow',
    label: 'Москва'
  },
  {
    value: 'saint-petersburg',
    label: 'Санкт-Петербург'
  },
  {
    value: 'kazan',
    label: 'Казань'
  },
  {
    value: 'rostov',
    label: 'Ростов-на-Дону'
  },
  {
    value: 'ekaterinburg',
    label: 'Екатеринбург'
  },
  {
    value: 'volgograd',
    label: 'Волгоград'
  },
  {
    value: 'omsk',
    label: 'Омск'
  },
  {
    value: 'novosibirsk',
    label: 'Новосибирск'
  }
];

export const LocationSelect = () => {
  const [currentLocation, setCurrentLocation] = useState('ekaterinburg');

  const getValue = () => {
    return currentLocation ? options.find((loc) => loc.value === currentLocation) : '';
  };

  const onChange = (newValue: unknown) => {
    setCurrentLocation((newValue as AppSelectOption).value);
  };

  return <AppSelect options={options} onChange={onChange} value={getValue()} />;
};
