// Capture helper — records a 6 s loop of the iframe's <canvas> as a WebM blob.
// Strategy:
//   1. Reach into the iframe's contentWindow and call its window.captureLoop(seconds)
//      if the artifact exposes one (preferred — the artifact controls timing).
//   2. Otherwise, find the <canvas> inside the iframe and record it via captureStream.
// Same-origin assumed (preview server serves both /preview and /concepts).

window.captureFromIframe = async function (iframeEl, seconds = 6.0) {
  const w = iframeEl.contentWindow;
  if (!w) throw new Error('iframe contentWindow not accessible');

  if (typeof w.captureLoop === 'function') {
    const blob = await w.captureLoop(seconds);
    if (blob instanceof Blob) return blob;
  }

  const doc = w.document;
  const canvas = doc && doc.querySelector('canvas');
  if (!canvas) throw new Error('no <canvas> found inside artifact iframe');

  const stream = canvas.captureStream(60);
  const mime = MediaRecorder.isTypeSupported('video/webm;codecs=vp9')
    ? 'video/webm;codecs=vp9'
    : 'video/webm';
  const recorder = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: 8_000_000 });

  return new Promise((resolve, reject) => {
    const chunks = [];
    recorder.ondataavailable = (e) => { if (e.data && e.data.size) chunks.push(e.data); };
    recorder.onerror = (e) => reject(e.error || new Error('MediaRecorder error'));
    recorder.onstop = () => resolve(new Blob(chunks, { type: 'video/webm' }));
    recorder.start();
    setTimeout(() => recorder.stop(), Math.max(500, seconds * 1000));
  });
};
