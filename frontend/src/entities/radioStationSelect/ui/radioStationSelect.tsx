import { AppSelect, AppSelectOption } from 'shared/ui/appSelect';
import { useRadioStore } from 'shared/store';
import { useDefaultRadios } from '../hooks';

export const RadioStationSelect = () => {
  const { radios, selectedRadioId, setSelectedRadioId } = useRadioStore();

  const { isLoading } = useDefaultRadios();

  const options = radios.map((radio) => ({ value: radio.id.toString(), label: radio.name }));

  const getValue = () => {
    return selectedRadioId ? options.find((radio) => radio.value === selectedRadioId.toString()) : '';
  };

  const onChange = (newValue: unknown) => {
    const selectedRadio = radios.find((radio) => radio.id.toString() === (newValue as AppSelectOption).value);
    if (selectedRadio) {
      setSelectedRadioId(selectedRadio.id);
    }
  };

  return (
    <AppSelect
      placeholder={isLoading ? 'Загрузка ...' : options.length ? 'Выберите радио' : 'Нет доступных'}
      maxWidth={'275px'}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
