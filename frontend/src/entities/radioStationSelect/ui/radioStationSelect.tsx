import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';
import { useOrderStore, useRadioStore } from 'shared/store';
import { useDefaultRadios } from '../hooks';

export const RadioStationSelect = () => {
  const { isLoading } = useDefaultRadios();
  const { clearCustomerSelections } = useOrderStore();
  const { radios, selectedRadioId, setSelectedRadioId } = useRadioStore();

  const options = radios.map((radio) => ({ value: radio.id.toString(), label: radio.name }));

  const getValue = () => {
    return selectedRadioId ? options.find((radio) => radio.value === selectedRadioId.toString()) : '';
  };

  const onChange = (newValue: unknown) => {
    const selectedRadio = radios.find((radio) => radio.id.toString() === (newValue as AppSelectOption).value);
    if (selectedRadio) {
      setSelectedRadioId(selectedRadio.id);
      clearCustomerSelections();
    }
  };

  return (
    <AppSelect
      placeholder={isLoading ? 'Загрузка ...' : options.length ? 'Выберите радио' : 'Нет доступных'}
      maxWidth={'100%'}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
