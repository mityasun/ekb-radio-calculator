import { AppSelect } from 'shared/ui/appSelect';
import { useStore } from 'shared/store';
import { useDefaultRadios } from '../hooks';
import { AppSelectOption } from 'shared/types';
import { RADIO_STATION_CONTENT_TEXT, maxWidth } from '../configs';

export const RadioStationSelect = () => {
  const { radios, isLoading } = useDefaultRadios();
  const { selectedRadioId, setSelectedRadioId } = useStore();

  if (!radios) return null;

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
      placeholder={
        isLoading
          ? RADIO_STATION_CONTENT_TEXT.LOADING
          : options.length
            ? RADIO_STATION_CONTENT_TEXT.SELECT_RADIO
            : RADIO_STATION_CONTENT_TEXT.NO_AVAILABLE
      }
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
