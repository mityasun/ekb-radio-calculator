import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';
import { useCityStore } from 'shared/store';
import { useDefaultCity } from '../hooks';

export const LocationSelect = () => {
  const { cities, selectedCity, setSelectedCity } = useCityStore();

  useDefaultCity();

  const options = cities.map((city) => ({ value: city.id.toString(), label: city.name }));

  const getValue = () => {
    return selectedCity ? options.find((loc) => loc.value === selectedCity.id.toString()) : '';
  };

  const onChange = (newValue: unknown) => {
    const selectedCity = cities.find((city) => city.id.toString() === (newValue as AppSelectOption).value);
    if (selectedCity) {
      setSelectedCity(selectedCity);
    }
  };

  return <AppSelect maxWidth={'275px'} options={options} onChange={onChange} value={getValue()} />;
};
