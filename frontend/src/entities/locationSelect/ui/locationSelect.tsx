import { AppSelect } from 'shared/ui/appSelect';
import { useCityStore, useOrderStore } from 'shared/store';
import { useDefaultCity } from '../hooks';
import { AppSelectOption } from 'shared/types';

export const LocationSelect = () => {
  const { isLoading, cities } = useDefaultCity();
  const { clearCustomerSelections } = useOrderStore();
  const { selectedCity, setSelectedCity } = useCityStore();

  if (!cities) return;

  const options = cities.map((city) => ({ value: city.id.toString(), label: city.name }));

  const getValue = () => {
    return selectedCity ? options.find((loc) => loc.value === selectedCity.id.toString()) : '';
  };

  const onChange = (newValue: unknown) => {
    const selectedCity = cities.find((city) => city.id.toString() === (newValue as AppSelectOption).value);
    if (selectedCity) {
      setSelectedCity(selectedCity);
      clearCustomerSelections();
    }
  };

  return (
    <AppSelect
      placeholder={isLoading ? 'Загрузка ...' : options.length ? 'Выберите город' : 'Нет доступных'}
      maxWidth={'100%'}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
