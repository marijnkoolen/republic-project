import {memo, MutableRefObject} from "react";
import moment from "moment";
import 'moment/locale/nl'
import {HistogramBar} from "../../common/Histogram";
import {useResolutionContext} from "../../resolution/ResolutionContext";
import {useAsyncError} from "../../hook/useAsyncError";
import {fromEsFormat} from "../../util/fromEsFormat";
import {useClientContext} from "../../elastic/ClientContext";
import {equal} from "../../util/equal";
import {HISTOGRAM_PREFIX} from "../../content/Placeholder";
import Place from "../model/Place";
import {C5} from "../../style/Colors";
import {usePlotContext} from "../../plot/PlotContext";
import renderPlot from "../../plot/Plot";

moment.locale('nl');

type PlaceHistogramProps = {
  svgRef: MutableRefObject<any>,
  handleResolutions: (r: string[]) => void,
  place: Place,
  memoKey: any
}

/**
 * Bar chart rendered on svgRef
 */
export const PlaceHistogram = memo(function (props: PlaceHistogramProps) {

  const {resolutionState} = useResolutionContext();
  const throwError = useAsyncError();
  const client = useClientContext().clientState.client;
  const {plotState} = usePlotContext();

  updateHistogram();

  function updateHistogram() {

    const bars = resolutionState.resolutions;

    if (!bars.length) {
      return;
    }

    client.resolutionResource.aggregateByPlace(
      bars.reduce((all, arr: HistogramBar) => all.concat(arr.ids), [] as string[]),
      props.place,
      fromEsFormat(bars[0].date),
      fromEsFormat(bars[bars.length - 1].date)
    ).then((buckets: any) => {
      const bars = buckets.map((b: any) => ({
        date: b.key_as_string,
        count: b.doc_count,
        ids: b.resolution_ids.buckets.map((b: any) => b.key)
      } as HistogramBar));

      renderPlot(
        plotState.type,
        props.svgRef,
        bars,
        { color: C5, y: { title: `${HISTOGRAM_PREFIX} ${props.place.val}`}},
        props.handleResolutions
      );

    }).catch(throwError);
  }

  return null;

}, (prev, next) => equal(prev.memoKey, next.memoKey));
