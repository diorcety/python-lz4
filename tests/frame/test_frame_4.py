from . helpers import roundtrip_LZ4FrameCompressor
import os
import pytest

test_data=[
    (os.urandom(128 * 1024)),
    (os.urandom(256 * 1024)),
    (os.urandom(512 * 1024)),
    (os.urandom(1024 * 1024)),
]

@pytest.fixture(
    params=test_data,
    ids=[
        'data' + str(i) for i in range(len(test_data))
    ]
)
def data(request):
    return request.param

@pytest.fixture(
    params=[
        (True),
        (False)
    ]
)
def reset(request):
    return request.param

@pytest.fixture(
    params=[
        (1),
        (8)
    ]
)
def chunks(request):
    return request.param


def test_roundtrip_LZ4FrameCompressor(data, chunks, block_size, reset):
    roundtrip_LZ4FrameCompressor(
        data,
        chunks=chunks,
        block_size=block_size,
        reset=reset
    )



#     def test_LZ4FrameCompressor_reset(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         with lz4frame.LZ4FrameCompressor() as compressor:
#             compressed = compressor.compress_begin()
#             compressed += compressor.compress(input_data)
#             compressed += compressor.flush()
#             compressor.reset()
#             compressed = compressor.compress_begin()
#             compressed += compressor.compress(input_data)
#             compressed += compressor.flush()
#         decompressed = lz4frame.decompress(compressed)
#         self.assertEqual(input_data, decompressed)

#     def test_compress_without_content_size(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         compressed = lz4frame.compress(input_data, content_size_header=False)
#         frame = lz4frame.get_frame_info(compressed)
#         self.assertEqual(frame['contentSize'], 0)
#         decompressed = lz4frame.decompress(compressed)
#         self.assertEqual(input_data, decompressed)

#     def test_LZ4FrameCompressor2(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         with lz4frame.LZ4FrameCompressor() as compressor:
#             compressed = compressor.compress_begin()
#             compressed += compressor.compress(input_data)
#             compressed += compressor.flush()
#         dctx = lz4frame.create_decompression_context()
#         decompressed, read = lz4frame.decompress2(dctx, compressed, full_frame=True)
#         self.assertEqual(input_data, decompressed)
#         self.assertEqual(read, len(compressed))

#     def test_LZ4FrameCompressor2b(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         with lz4frame.LZ4FrameCompressor() as compressor:
#             compressed = compressor.compress_begin()
#             compressed += compressor.compress(input_data)
#             compressed += compressor.flush()
#         mid = int(len(compressed) / 2)
#         dctx = lz4frame.create_decompression_context()
#         decompressed, read = lz4frame.decompress2(dctx, compressed[0:mid])
#         decompressed, r = lz4frame.decompress2(dctx, compressed[read:])
#         read += r
#         self.assertEqual(input_data, decompressed)
#         self.assertEqual(read, len(compressed))

#     def test_LZ4FrameCompressor2b(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         with lz4frame.LZ4FrameCompressor() as compressor:
#             compressed = compressor.compress_begin()
#             compressed += compressor.compress(input_data)
#             compressed += compressor.flush()
#         mid = int(len(compressed) / 2)
#         with lz4frame.LZ4FrameDecompressor() as decompressor:
#             decompressed, read = decompressor.decompress(compressed[0:mid])
#             decompressed, r = decompressor.decompress(compressed[read:])
#             read += r
#         self.assertEqual(input_data, decompressed)
#         self.assertEqual(read, len(compressed))


# class TestLZ4FrameModern(unittest.TestCase):
#     def test_decompress_truncated(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         for chksum in (lz4frame.CONTENTCHECKSUM_DISABLED, lz4frame.CONTENTCHECKSUM_ENABLED):
#             for conlen in (0, len(input_data)):
#                 context = lz4frame.create_compression_context()
#                 compressed = lz4frame.compress_begin(context, content_checksum=chksum, source_size=conlen)
#                 compressed += lz4frame.compress_update(context, input_data)
#                 compressed += lz4frame.compress_end(context)
#                 for i in range(len(compressed)):
#                     with self.assertRaisesRegexp(RuntimeError, r'^(LZ4F_getFrameInfo failed with code: ERROR_frameHeader_incomplete|LZ4F_freeDecompressionContext reported unclean decompressor state \(truncated frame\?\): \d+)$'):
#                         lz4frame.decompress(compressed[:i])

#     def test_checksum_failure(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         compressed = lz4frame.compress(input_data, content_checksum=lz4frame.CONTENTCHECKSUM_ENABLED)
#         with self.assertRaisesRegexp(RuntimeError, r'^LZ4F_decompress failed with code: ERROR_contentChecksum_invalid'):
#             last = struct.unpack('B', compressed[-1:])[0]
#             lz4frame.decompress(compressed[:-1] + struct.pack('B', last ^ 0x42))
#         # NB: blockChecksumFlag is not supported by lz4 at the moment, so some
#         # random 1-bit modifications of input may actually trigger valid output
#         # without errors. And content checksum remains the same!

#     def test_decompress_trailer(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         compressed = lz4frame.compress(input_data)
#         with self.assertRaisesRegexp(ValueError, r'^Extra data: 64 trailing bytes'):
#             lz4frame.decompress(compressed + b'A'*64)
#         # This API does not support frame concatenation!
#         with self.assertRaisesRegexp(ValueError, r'^Extra data: \d+ trailing bytes'):
#             lz4frame.decompress(compressed + compressed)

#     def test_LZ4FrameCompressor_fails(self):
#         input_data = b"2099023098234882923049823094823094898239230982349081231290381209380981203981209381238901283098908123109238098123"
#         with self.assertRaisesRegexp(RuntimeError, r'compress called after flush'):
#             with lz4frame.LZ4FrameCompressor() as compressor:
#                 compressed = compressor.compress_begin()
#                 compressed += compressor.compress(input_data)
#                 compressed += compressor.flush()
#                 compressed = compressor.compress(input_data)


# if sys.version_info < (2, 7):
#     # Poor-man unittest.TestCase.skip for Python 2.6
#     del TestLZ4FrameModern

# if __name__ == '__main__':
#     unittest.main()
