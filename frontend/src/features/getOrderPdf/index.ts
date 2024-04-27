import { AdSettings, CityModel, CustomerSelection, OrderPdf, RadioModel } from 'shared/types';

export type GetOrderPdfProps = {
  selectedCity?: CityModel | null;
  selectedRadio?: RadioModel | null;
  adSettings?: AdSettings;
  customer_selection?: CustomerSelection[];
};

export const getResponseOrderPdf = ({
  selectedCity,
  selectedRadio,
  adSettings,
  customer_selection
}: GetOrderPdfProps) => {
  if (
    !selectedCity ||
    !selectedRadio ||
    !adSettings?.month ||
    !adSettings.block_position ||
    !customer_selection?.length
  )
    return;

  const response: OrderPdf = {
    city: selectedCity.id,
    station: selectedRadio.id,
    month: adSettings.month.id,
    block_position: adSettings.block_position.id,
    other_person_rate: adSettings.other_person_rate,
    hour_selected_rate: adSettings.hour_selected_rate,
    customer_selection: customer_selection.map((selection) => ({
      ...selection,
      audio_duration: selection.audio_duration
    }))
  };

  return response;
};
