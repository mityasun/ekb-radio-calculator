import { AppSelect } from 'shared/ui/appSelect';
import { useStore } from 'shared/store';
import { useDefaultCity } from '../hooks';
import { AppSelectOption } from 'shared/types';
import { LOCATION_CONTENT_TEXT, maxWidth } from '../configs';

export const LocationSelect = () => {
  const { isLoading, cities } = useDefaultCity();
  const { selectedCity, setSelectedCity, clearCustomerSelections } = useStore();

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
      placeholder={
        isLoading
          ? LOCATION_CONTENT_TEXT.LOADING
          : options.length
            ? LOCATION_CONTENT_TEXT.SELECT_LOCATION
            : LOCATION_CONTENT_TEXT.NO_AVAILABLE
      }
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
