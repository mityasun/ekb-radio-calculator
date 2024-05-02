import { AppSettings, CityModel, CustomerSelection, OrderPdf, RadioModel } from 'shared/types';

export type postOrderPdfProps = {
  selectedCity?: CityModel | null;
  selectedRadio?: RadioModel | null;
  appSettings?: AppSettings;
  customer_selection?: CustomerSelection[];
};

export const getResponseOrderPdf = ({
  selectedCity,
  selectedRadio,
  appSettings,
  customer_selection
}: postOrderPdfProps) => {
  if (
    !selectedCity ||
    !selectedRadio ||
    !appSettings?.month ||
    !appSettings.block_position ||
    !customer_selection?.length
  )
    return;

  const response: OrderPdf = {
    city: selectedCity.id,
    station: selectedRadio.id,
    month: appSettings.month.id,
    block_position: appSettings.block_position.id,
    other_person_rate: appSettings.other_person_rate,
    hour_selected_rate: appSettings.hour_selected_rate,
    customer_selection: customer_selection.map((selection) => ({
      ...selection,
      audio_duration: selection.audio_duration
    }))
  };

  return response;
};
