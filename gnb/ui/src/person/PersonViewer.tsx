import {D3Canvas} from "../common/D3Canvas";
import PersonHistogram from "./PersonHistogram";
import TextsModal from "../common/Texts";
import React, {memo, useEffect, useRef, useState} from "react";
import {Person} from "../elastic/model/Person";
import {PersonType} from "../elastic/model/PersonType";
import {equal} from "../util/equal";

type PersonViewerProps = {
  person: Person,
  type: PersonType
  memoOn: any
}

export default memo(function PersonViewer(props: PersonViewerProps) {

  const svgRef = useRef(null);
  const [hasSvg, setHasSvg] = useState(svgRef.current);

  const [state, setState] = React.useState({
    ids: [] as string[],
    showTexts: false
  });

  useEffect(() => {
    setHasSvg(svgRef.current)
  }, [svgRef]);

  return <>
    <D3Canvas svgRef={svgRef}/>

    {hasSvg ? <PersonHistogram
      handleResolutions={(ids: string[]) => setState({...state, ids, showTexts: true})}
      svgRef={svgRef}
      person={props.person}
      type={props.type}
      memoOn={props.memoOn}
    /> : null}

    <TextsModal
      resolutions={state.ids}
      isOpen={state.showTexts}
      handleClose={() => setState({...state, showTexts: false})}
    />
  </>

}, ((prev, next) => equal(prev.memoOn, next.memoOn)));
